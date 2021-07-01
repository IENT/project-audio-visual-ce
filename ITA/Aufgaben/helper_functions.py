# +++++ HELPER FUNCTIONS ++++++
import os
from pathlib import Path
import numpy as np
from scipy import spatial
from scipy.signal import butter, filtfilt
import matplotlib.pyplot as plt
from scipy.io import wavfile


def get_HRIR_at_direction(HRIR_dataset, azimuth, elevation):
    """
    Get the HRIR for a specified dataset and direction.
    It selects the nearest direction and selects the corresponding HRIR.

    Parameters
    ----------
    HRIR_dataset : sofa.Database
        The HRIR dataset, containing all directions.
    direction : list [theta, phi]
        The direction to extract a two-channel HRIR from.

    Returns
    -------
    HRIR : numpy.ndarray
        The two-channel HRIR for the specified direction.
    idx : integer
        The index of the HTRF, corresponding to the input direction.
    actual_direction : list [theta, phi]
        The actual direction (sampling positions are discrete!).
    """
    # get the index of the position with minimal distance:
    # get the source positions from the HRIR dataset in 
    # spherical coordinates (use degrees):
    source_positions = HRIR_dataset.Source.Position.get_values(
        indices={"M": slice(None)}, system="spherical", angle_unit="degree")

    # throw away the distance (only direction is important here):
    source_directions = source_positions[:, 0:2]

    # get the index of the position with minimal distance:
    kd_tree = spatial.KDTree(source_directions)
    distance, idx = kd_tree.query([azimuth, elevation])

    # get the actual direction, which might deviate from the given:
    actual_direction = source_directions[idx]

    # for each of the channels (2 ears), extract the respective HRIR
    HRIR = np.zeros([2, HRIR_dataset.Dimensions.N])
    for receiver in np.arange(HRIR_dataset.Dimensions.R):
        HRIR[receiver, :] = HRIR_dataset.Data.IR.get_values(
            indices={"M": idx, "R": receiver, "E": 0})

    return HRIR


def plot_HRIR(HRIR, ILD, ITD, sampling_rate=44100):
    """
    Plot the given HRIR while visualizing its ILD and ITD.

    Parameters
    ----------
    HRIR : numpy.ndarray
        The HRIR for a single direction.
    sampling_rate : integer
        The sampling rate of the HRIR.
    """
    # get the time vector for plotting
    n_samples = HRIR.shape[-1]
    t = np.arange(0, n_samples)/sampling_rate

    # create the figure and axes
    fig, ax = plt.subplots(1, 2, figsize=(15, 4))

    # get the data for the time plot:

    # calculate the values in decibels
    dB_data = 20*np.log10(np.abs(HRIR))
    # lowpass filtering of the data for smooth plot
    # dB_data = butter_lowpass_filter(dB_data, 44100, 10000, 2)

    # plot the two channels
    ax[0].plot(t, dB_data[0], label='Left Ear')
    ax[0].plot(t, dB_data[1], label='Right Ear')

    # visualize the ILD and ITD
    ax[0].axvspan(
        t[np.argmax(dB_data[0])], t[np.argmax(dB_data[1])],
        alpha=0.5,
        color='yellow',
        label='ITD')

    # set limits, title, labels and activate legend
    ax[0].set_ylim(-60, 10)
    ax[0].set_xlim(0, t[-1])
    ax[0].set_xlabel('Time [s]')
    ax[0].set_ylabel('HRIR [dB]')
    fig.suptitle('ITD: ' + str(np.round(ITD*1000, 2)) +
                 'ms' + '          ILD: ' + str(np.round(ILD, 2)) + 'dB')
    ax[0].legend()

    # get the data for the magnitude plot:
    data_dB_freq_L = 20*np.log10(
        np.abs(np.fft.rfft(HRIR[0], n=n_samples, axis=-1))/20)
    data_dB_freq_R = 20*np.log10(
        np.abs(np.fft.rfft(HRIR[1], n=n_samples, axis=-1))/20)

    frequencies = np.fft.rfftfreq(n_samples, d=1/sampling_rate)

    ax[1].semilogx(frequencies, data_dB_freq_L.T, label='Left Ear')
    ax[1].semilogx(frequencies, data_dB_freq_R.T, label='Right Ear')

    ax[1].set_xlabel("Frequency [Hz]")
    ax[1].set_ylabel("Magnitude [dB]")

    ax[1].set_xscale('log')
    ax[1].grid(True, 'both')

    ax[1].set_ylim((-60, 10))
    ax[1].set_xlim((20, sampling_rate/2))
    ax[1].fill_between(
        frequencies,
        data_dB_freq_L.T,
        data_dB_freq_R.T,
        alpha=0.25,
        color='red',
        label='ILD')
    ax[1].legend()


def plot_HRIR_at_direction(
        HRIR_dataset,
        azimuth,
        elevation,
        ILD_function,
        ITD_function):
    """
    Plot the HRIR for a given direction while visualizing its ILD and ITD.

    Parameters
    ----------
    HRIR : numpy.ndarray
        The HRIR for a single direction.
    azimuth : double
        The azimuth angle in degrees to extract the HRIR from.
    elevation : double
        The elevation angle in degrees to extract the HRIR from.
    """
    sampling_rate = HRIR_dataset.Data.SamplingRate.get_values(indices={"M": 0})
    HRIR = get_HRIR_at_direction(HRIR_dataset, azimuth, elevation)
    plot_HRIR(HRIR, ILD_function(HRIR), ITD_function(HRIR), sampling_rate)


def butter_lowpass_filter(data, fs, cutoff, order):
    """
    Filters the data using a butterworth lowpass filter.

    Parameters
    ----------
    data : numpy.ndarray
        The input sequence.
    fs : integer
        The sampling rate.
    cutoff : double
        The cutoff frequency of the filter.
    order : integer
        The order of the filter.

    Returns
    -------
    y : numpy.ndarray
        The filtered sequence.
    """
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y


def normalize(x):
    """
    Normalizes an array by dividing by its largest absolute value.

    Parameters
    ----------
    x : numpy.ndarray
        Input array.

    Returns
    -------
    numpy.ndarray
        Normalized array.
    """
    return x/np.amax(np.abs(x))


def read_wav(filepath):
    return pcm2float(wavfile.read(filepath)[1])


def write_wav(data, filepath, sampling_rate=44100):
    """Save a numpy array as a wav file.

    Parameters
    ----------
    data : numpy.ndarray
        The data to be saved with shape (num_channels, num_samples)
    filename : string, path
        A string containing the path and filename
    """
    head = os.path.split(filepath)[0]
    if not os.path.exists(head):
        os.makedirs(head)
    wavfile.write(filepath, sampling_rate, float2pcm(data.T))


def pcm2float(sig):
    """Convert PCM signal to floating point with a range from -1 to 1.

    Parameters
    ----------
    sig : numpy.ndarray
        Input array, must have integral type.

    Returns
    -------
    numpy.ndarray
        Normalized floating point data.
    """
    sig = np.asarray(sig)
    if sig.dtype.kind not in 'iu':
        raise TypeError("'sig' must be an array of integers")
    dtype = np.dtype('float64')
    i = np.iinfo(sig.dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig.astype(dtype) - offset) / abs_max


def float2pcm(sig):
    """Convert floating point signal with a range from -1 to 1 to PCM.
    Any signal values outside the interval [-1.0, 1.0) are clipped.
    No dithering is used.

    Parameters
    ----------
    sig : numpy.ndarray
        Input array, must have floating point type.

    Returns
    -------
    numpy.ndarray
        Integer data, scaled and clipped to the range of the given
        *dtype*.
    """
    sig = np.asarray(sig)
    if sig.dtype.kind != 'f':
        raise TypeError("'sig' must be a float array")
    dtype = np.dtype('int16')
    i = np.iinfo(dtype)
    abs_max = 2 ** (i.bits - 1)
    offset = i.min + abs_max
    return (sig * abs_max + offset).clip(i.min, i.max).astype(dtype)


def linear_interpolation(signal, times, sampling_rate=44100):
    """
    Linear interpolation of the given `signal` at `times`.

    Parameters
    ----------
    signal : numpy.ndarray
        Input sequence array.
    times : numpy.ndarray
        Array of time instances.
    sampling_rate : integer
        The sampling rate.

    Returns
    -------
    result : numpy.ndarray
        Output array containing the interpolation.
    """
    # create an array containing all indices
    indices = np.arange(0, signal.shape[-1], 1)
    # shift the indices as defined in the times vector
    warped_indices = indices - times * sampling_rate
    # floor those indices
    floored_indices = np.floor(warped_indices).astype(int)
    remaining = warped_indices - floored_indices
    result = (((1-remaining) * signal[:, floored_indices]
               + remaining * signal[:, (floored_indices+1)]) 
              * (floored_indices >= 0))
    shift = floored_indices[floored_indices < 0].shape[-1]
    result = result[:, shift:-1]
    return result
