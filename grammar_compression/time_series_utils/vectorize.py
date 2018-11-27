"""
Vectorized calculations for improved performance when performing full time 
series calculations.
"""
import numpy as np
from time_series_utils.time_series import Subsequence

def calculate_subsequence_distances(T,n):
    """Calculate the distance between every pair of subsequences, B and C."""
    # m-n+1 total subsequences gives an (n x m-n+1) array
    m = T.length
    subsequence_obs = np.array([T.obs[i:i+n] for i in range(m-n+1)])
    # Reshape the subsequences for a vectorized distance calculation
    C = subsequence_obs.reshape((m-n+1,1,n))
    D = subsequence_obs.reshape((1,m-n+1,n))
    distances = np.linalg.norm(C-D,axis=2)
    return distances

def keep_distance_below_threshold(h,distances):
    """Convert distances above threshold value into NaNs to be ignored."""
    distances[distances > h] = np.nan
    return distances

def remove_selfmatch(T,n,distances):
    """Convert self-matches into NaNs to be ignored."""
    m = T.length
    for i in range(len(distances)):
        for j in range(len(distances[0])):
            if np.abs(i-j) <= n:
                distances[i,j] = np.nan
    return distances

def handle_subsequences_with_no_matches(distances):
    """Clean data so that rows with all NaNs do not break min/max functions."""
    # Find rows with all NaNs
    nan_rows = np.all(np.isnan(distances),axis=1)
    # Replace the last element of all-NaN rows with -np.inf
    nan_row_elements = np.array(np.zeros_like(distances),dtype=bool)
    nan_row_elements[:,-1] = nan_rows
    distances[nan_row_elements] = -np.inf
    return distances
           
def get_nearest_neighbors(distances):
    """Get locations of the nearest neighbor from every subsequence."""
    # Nearest neighbor is the subsequence with the smallest distance
    nearest_neighbor_dists = np.nanmin(distances,axis=1)
    nearest_neighbor_dists = nearest_neighbor_dists.reshape(len(distances),1)
    nearest_neighbors = (distances==nearest_neighbor_dists)
    return nearest_neighbors

def get_furthest_nearest_neighbor(distances):
    """Get the index of the subsequence with the furthest nearest neighbor."""
    nearest_neighbors = get_nearest_neighbors(distances)
    furthest_nearest_neighbor_dist = np.amax(distances[nearest_neighbors])
    if furthest_nearest_neighbor_dist == -np.inf:
        raise ValueError('The threshold was too small, no non-self-matches found.')
    # Find the furthest pair of subsequences among the nearest neighbors
    furthest_pair = (distances==furthest_nearest_neighbor_dist)
    furthest_nearest_neighbor = (nearest_neighbors & furthest_pair)    
    # Convert the boolean map of the furthest nearest neighbor to an index
    indices = np.argwhere(furthest_nearest_neighbor)[:,0]
    return indices

def get_discords(T,n,h=None):
    """
    Get the discord(s) in a time series.
    
    Takes a time series T of length n and finds the discord(s) of T, where the 
    discord of T is the subsequence that is furthest from its nearest non-self-
    match. The nearest non-self-match of a subsequence is the non-self-match
    with the smallest distance between the non-self-match and the subsequence.

    Parameters
    ----------
    T : TimeSeries class
        The time series in which to find discords.
    n : int
        The length of time series T.
    h : float
        The threshold setting the maximum distance for which subsequences may
        still be considered matching.

    Returns
    -------
    discords : list of Subsequence class
        A set of subsequences that are discords of T.
    """
    distances = calculate_subsequence_distances(T,n)
    # Ignore disqualified subsequences
    if h:
        distances = keep_distance_below_threshold(h,distances)
    distances = remove_selfmatch(T,n,distances)
    distances = handle_subsequences_with_no_matches(distances)
    P = get_furthest_nearest_neighbor(distances) + 1
    # Convert indices to subsequences
    discords = [Subsequence(T,p,n) for p in P]
    return discords 
