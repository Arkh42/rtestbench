
# Scientific computations
import numpy
import pandas

# Plot library
import matplotlib.pyplot as plt

# Annotations
from typing import List
pd_list = List[pandas.Series]


def plot(x_data, n_bins=50, title='Histogram', **kwargs):
    """Plot the histogram.

    Assumes that data is a pandas' Series object.
    Reference: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.hist.html
    """

    plt.figure()

    plt.hist(x_data, n_bins, density=False, histtype='bar', align='mid', **kwargs)

    plt.xlabel(x_data.name)
    plt.ylabel('Counts')

    plt.title(title)

    plt.grid(True)

    # plt.show()
