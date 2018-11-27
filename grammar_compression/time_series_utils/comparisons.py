"""Utilities for working with time series."""
import numpy as np
import seaborn as sns
from time_series_utils.dist_functions import euc_dist
from time_series_utils.time_series import Subsequence
from matplotlib import pyplot as plt
# Change math font to Computer Modern (LaTeX default)
from matplotlib import rcParams
rcParams['mathtext.fontset'] = 'cm'

def match(d,h):
    """Check if a distance, d, is greater than the threshold, h."""
    return d <= h

def nonselfmatch(C,D,h=None,dist=euc_dist,use_z_norm=False):
    """
    Check if two subsequences, C and D, are non-self-matches.

    Function to check if subsequences C and D are non-self-matches. The function
    first checks if the subsequences overlap, and if they do not, it calculates 
    the distance between them.

    Parameters
    ----------
    C,D : Subsequence class 
        The subsequences to be checked as a potential matches.
    h : float
        The threshold setting the maximum distance for which subsequences may 
        still be considered matching.
    dist : function
        A function taking two subsequences as its arguments. The function must 
        return a  numeric distance between the two subsequences.
    use_z_norm : bool
        A flag indicating whether to use the z-normalized subsequences when 
        determining matches.

    Returns
    -------
    flag : bool
        True if the parameter is a non-self-match; False otherwise.
    """
    if C.length != D.length:
        raise ValueError('The subsequences must be the same length.')
    if np.abs(C.start-D.start) >= C.length:
        distance = dist(C,D,use_z_norm)
        if not h or match(distance,h):
            return True
    return False

def find_subsequence_nonselfmatches(C,h,dist=euc_dist,use_z_norm=False):
    """Find all non-self-matches to substring C in a time series."""
    m = C.parent.length
    n = C.length
    nonselfmatches = []
    for q in range(1,m-n+2):
        D = Subsequence(C.parent,q,n)
        if nonselfmatch(C,D,h,dist,use_z_norm):
            nonselfmatches.append(D)
    return nonselfmatches

def compare_subsequences(C,D,title=None,z_norm='none',dist=euc_dist):
    """
    Visually compare two subsequences, C and D, and give their distance.
    
    Parameters
    ----------
    C,D : Subsequence class
        Two subsequences to be compared.
    title : str, optional
        A title for the time series plot.
    znorm : str, optional
        A keyword giving the z-normalization of the distance calculation. 
        Options are:
             'series'       - z-normalize the entire time series
             'subsequences' - z-normalize each subsequence separately
             'none'         - do not z-normalize
    """
    if not C.parent is D.parent:
        raise ValueError('C and D must be subsequences of the same time series.')
    if C.length != D.length:
        raise ValueError('C and D must be subsequences of the same length.')
    # Visually compare subsequences C and D
    C.plot_timeseries(title)
    ax_comp = C.shade_subsequence()
    ax_comp = D.shade_subsequence(ax=ax_comp) 
    plt.show()
    # Give the Euclidean distance (based on type of znorm)
    if z_norm == 'series':
        T.z_normalize()
        C = Subsequence(T.z_norm,C.start,C.length)
        D = Subsequence(T.z_norm,D.start,D.length)
        output_label = 'Time series z-normalized distance:'
    if z_norm == 'subsequences':
        C.z_normalize()
        D.z_normalize()
        use_z_norm = True
        output_label = 'Subsequence z-normalized distance:'
    if z_norm == 'none':
        output_label = 'Subsequence distance:'
    print(output_label,round(dist(C,D,use_z_norm),3))

    
def plot_nonselfmatches(C,nonselfmatches,title=None,return_ax=False):
    """
    Plot a set of non-self-matches as shading on the time series.
    
    Given a subsequence C of length n starting at p, shade all non-self-matches 
    on the original time series T. Each non-self-match is a subsequence, D. 
    
    Parameters
    ----------
    C : Subsequence class
        The subsequence to find matches for.
    nonselfmatches : list of Subsequence class
        Subsequences that qualify as non-self-matches.
    title : str, optional
        A title for the time series plot.
    return_ax : bool
        Flag to set whether the function plots the figure or returns the axis
        object.
        
    Returns
    -------
    ax_nsm : axes_object
        If return_ax=True, ax_nsm is the axes object containing the shaded time 
        series.
    """
    C.plot_timeseries(title)
    ax_nsm = C.shade_subsequence(color='green')
    for D in nonselfmatches:
        ax_nsm = D.shade_subsequence(ax=ax_nsm)
    if not return_ax:
        plt.show()
    else:
        return ax_nsm
