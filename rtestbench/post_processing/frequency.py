
# Scientific computations
import numpy
import pandas
from scipy import signal

# Plot library
import matplotlib.pyplot as plt

# Annotations
from typing import List
pd_list = List[pandas.Series]

# Auto styles
from . import _auto_style


def plot_psd(data, NFFT='full', Fs=None, title='Power Spectral Density', show=False, **kwargs):
    """Plot the power spectral density of data.

    Reference: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.psd.html
    """

    plt.figure()

    if NFFT in ('full', 'whole'):
        NFFT = len(data)
    
    plt.psd(data, NFFT=NFFT, Fs=Fs, scale_by_freq=True, **kwargs)

    plt.title(title)

    plt.grid(True)

    if show:
        plt.show()

def multiplot_psd(data: pd_list, NFFT='full', Fs=None, title='Power Spectral Densities', **kwargs):
    """Plot the power spectral density of several signals passed in data.

    Assumes that y_data is a list of pandas' Series objects sharing the same frequency axis.
    Reference: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.psd.html
    """
    plt.figure()
    legend = list()
    index = 0

    for data in y_data:
        if NFFT in ('full', 'whole'):
            NFFT = len(data)
        plt.psd(data, NFFT=NFFT, Fs=Fs, scale_by_freq=True, ls=_auto_style.auto_linestyle[index])
        legend.append(data.name)
        index = index + 1

    plt.title(title)
    plt.legend(legend)

    plt.grid(True)


def remove_freq_from_fft(data: pandas.Series, freq):
    """Compute the FFT, nullify at the specified frequency, then returns the IFFT.

    Assumes that data is a pandas' Series object.
    Reference: https://matplotlib.org/api/_as_gen/matplotlib.pyplot.psd.html
    """
    fourier = numpy.fft.rfft(data)
    fourier[freq] = 0
    filtered_data = numpy.fft.irfft(fourier)

    label = "{} - {} Hz removed".format(data.name, freq)

    return pandas.Series(data=filtered_data, name=label)


def remove_freq_by_stopband_filter(t, x, freq, showFrequencyResponse=True):
    dt = t[2] - t[1]
    Fs = 1 / dt
    nyquist_F = Fs / 2

    b = [1, -2*numpy.cos(freq/nyquist_F), 1]
    a = [1, -2*0.9*numpy.cos(numpy.pi*freq/nyquist_F), 0.9*0.9]
    w, h = signal.freqz(b, a, worN=2**20)

    if showFrequencyResponse:
        fig, ax1 = plt.subplots()
        ax1.set_title('Digital filter frequency response')

        ax1.plot(w, 20 * numpy.log10(abs(h)), 'b')
        ax1.set_ylabel('Amplitude [dB]', color='b')
        ax1.set_xlabel('Frequency [rad/sample]')

        ax2 = ax1.twinx()
        angles = numpy.unwrap(numpy.angle(h))
        ax2.plot(w, angles, 'g')
        ax2.set_ylabel('Angle [rad]', color='g')

        ax2.grid()
        ax2.axis('tight')
        plt.show()

    y = signal.filtfilt(b, a, x)

    label = "{} - {} Hz filtered".format(x.name, freq)

    return pandas.Series(data=y, name=label)

