"""Class definitions for time series and subsequences."""
import seaborn as sns
from matplotlib import pyplot as plt
# Change math font to Computer Modern (LaTeX default)
from matplotlib import rcParams
rcParams['mathtext.fontset'] = 'cm'

class TimeSeries:
    
    def __init__(self,times,observations):
        """
        A time series.

        A set of times and observations that together represent a time series.
        
        Parameters
        ----------
        times : ndarray
            An array of times, one for each observation in `observations`.
        observations : ndarray
            An array of observations, one for each time in `times`.
        """
        if not len(times) == len(observations):
            raise ValueError('The set of times and observations must be the same length!')
        self.times = times
        self.obs = observations
        self.length = len(self.obs)
        self.mean = self.obs.mean()
        self.stdev = self.obs.std()
    
    def plot_timeseries(self,title=None):
        """Generate a time series scatter plot with an optional title."""
        self.fig,self.ax = plt.subplots(figsize=(15,4))
        self.ax.scatter(self.times,self.obs)
        if title:
            self.ax.set_title(title,fontsize=16)
        return self.ax
    
    def z_normalize(self):
        """Find the z-normalization of the time series."""
        self.z_norm = (self.obs - self.mean)/self.stdev


class Subsequence(TimeSeries):

    def __init__(self,time_series,start,length):
        """
        A subsequence of the complete time series.

        A subsequence of a time series, defined by its starting index and 
        length. This class inherits from the TimeSeries class.;
        
        Parameters
        ----------
        time_series : TimeSeries class
            A time series class defining the parent time series of the
            subsequence.
        start : int
            The starting index of the subsequence in the times series.
        length : int
            The length of the subsequence.
        """
        self.parent = time_series
        times = time_series.times[start-1:start+length-1]
        observations = time_series.obs[start-1:start+length-1]
        TimeSeries.__init__(self,times,observations)
        self.start = start
        self.end = start + length
        self.length = length
    
    def plot_timeseries(self,title=None):
        """Generate a time series scatter plot with an optional title."""
        self.fig,self.ax = plt.subplots(figsize=(15,4))
        self.ax.scatter(self.parent.times,self.parent.obs)
        if title:
            self.ax.set_title(title,fontsize=16)
        return self.ax
    
    def shade_subsequence(self,color='#34495e',ax=None):
        """Add shading to the plot between two times."""
        if not ax:
            ax = self.ax 
        ax.axvspan(self.start,self.end,alpha=0.25,color=color)
        return ax

