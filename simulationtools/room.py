import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io import wavfile

from simulationtools import room_builder as room_builder, doa_module_wrapper as doa_wrapper
from utils import processing

# == data to plot ==
master_plot       = 0
plot_rir          = 0
plot_room         = 0
plot_doa_radar    = 0
plot_spectrogram1 = 0
plot_spectrogram2 = 0
# ==================


def receive_angles(mic_location, source1, source2=None):
    # prepare initial variables
    src_count = 1
    sound_file_path_female = "src/female.wav"
    sample_fs, voice_sample_female = wavfile.read(sound_file_path_female)
    voice_sample_female = voice_sample_female[:120000]

    sound_file_path_male = "src/male_fr.wav"
    sample_fs, voice_sample_male = wavfile.read(sound_file_path_male)
    voice_sample_male = voice_sample_male[40000:160000]

    absorption_factor = 0.85
    fs = 44100
    nsamples = 2048
    # end of init variables

    # prepare a room
    room_dimensions = [6.0, 8.0, 3.8]

    builder = room_builder.RoomBuilder(room_dimensions, fs, absorption_factor=absorption_factor,
                                       mic_location_array=mic_location)
    builder.add_sources(sources_array=source1, voice_sample=voice_sample_female, delay=0.2)
    room = builder.get_room()

    if source2 is not None:
        src_count = 2
        builder.add_sources(sources_array=source2, voice_sample=voice_sample_male)

    room.simulate()

    mic0_processed_signal = processing.convert_float_signal_to_int(room.mic_array.signals[0, :])
    mic1_processed_signal = processing.convert_float_signal_to_int(room.mic_array.signals[1, :])
    mic2_processed_signal = processing.convert_float_signal_to_int(room.mic_array.signals[2, :])
    mic3_processed_signal = processing.convert_float_signal_to_int(room.mic_array.signals[3, :])
    wavfile.write("mic0_record", 44100, mic0_processed_signal)

    # STFT
    f1, t1, stft_signal1 = signal.stft(mic0_processed_signal, fs=sample_fs, nperseg=nsamples)
    _, _, stft_signal2 = signal.stft(mic1_processed_signal, fs=sample_fs, nperseg=nsamples)
    _, _, stft_signal3 = signal.stft(mic2_processed_signal, fs=sample_fs, nperseg=nsamples)
    _, _, stft_signal4 = signal.stft(mic3_processed_signal, fs=sample_fs, nperseg=nsamples)

    # DOA
    input_doa_signal = np.vstack([stft_signal1[np.newaxis, :], stft_signal2[np.newaxis, :], stft_signal3[np.newaxis, :], stft_signal4[np.newaxis, :]])

    # create DOA module
    doa_module = doa_wrapper.DoaModuleWrapper(mic_location, room.fs, nsamples, src_count=src_count,
                                              option=doa_wrapper.DoaModuleWrapper.DoaOption.MUSIC)
    doa_module.calculate_doa(x_numpy_array=input_doa_signal)
    print("Calculated angle = " + str(doa_module.get_angle()))

    if plot_doa_radar: doa_module.plot_doa()

    if plot_spectrogram1:
        plt.figure("Spectrogram1")
        plt.pcolormesh(t1, f1, np.abs(stft_signal1))

    if plot_spectrogram2:
        plt.figure("Spectrogram2")
        plt.specgram(mic0_processed_signal, Fs=sample_fs)

    if plot_room:
        room.plot(img_order=1, aspect='equal')
        plt.xlabel("x axis")
        plt.ylabel("y axis")

    if plot_rir:
        plt.figure("rir")
        room.plot_rir()

    if master_plot:
        plt.show()

    return doa_module.get_angle()
