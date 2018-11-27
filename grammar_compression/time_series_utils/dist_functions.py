"""Distance functions to be used with time series."""
import numpy as np

def euc_dist(C,D,use_z_norm=False):
    """Calculate the Euclidean distance between any two subsequences."""
    if use_z_norm:
        return np.linalg.norm(C.z_norm-D.z_norm)
    return np.linalg.norm(C.obs-D.obs)
