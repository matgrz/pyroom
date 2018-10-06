import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.io import wavfile

import doa_module_wrapper as doa_wrapper
import room_builder as room_builder
from utils import processing

# == data to plot ==
master_plot       = 0
plot_rir          = 0
plot_room         = 1
plot_spectrogram1 = 0
plot_spectrogram2 = 0
# ==================


def receive_angles(mic_location, source1, source2=None):
    # prepare initial variables
    src_count = 1
    sound_file_path_female = "src/female.wav"
    sample_fs, voice_sample_female = wavfile.read(sound_file_path_female)
    voice_sample_female = voice_sample_female[:180000]

    sound_file_path_male = "src/male.wav"
    sample_fs, voice_sample_male = wavfile.read(sound_file_path_male)
    voice_sample_male = voice_sample_male[:180000, 0]

    absorption_factor = 0.99
    fs = 44100
    # end of init variables

    # prepare a room
    floor = np.array([[0, 0, 6, 6],
                      [0, 8, 8, 0]])

    builder = room_builder.RoomBuilder(floor, fs, absorption_factor, height=3.5, sources_array=source1,
                                       file_path=sound_file_path_female, mic_location_array=mic_location)
    builder.add_sources(sources_array=source1, voice_sample=voice_sample_female)
    room = builder.get_room()

    if source2 is not None:
        src_count = 2
        builder.add_sources(sources_array=source2, voice_sample=voice_sample_male)

    # source signal convolution
    room.compute_rir()
    room.simulate()

    #######
    mic0_processed_signal = processing.convert_float_signal_to_int(room.mic_array.signals[0, :])
    mic1_processed_signal = processing.convert_float_signal_to_int(room.mic_array.signals[1, :])
    wavfile.write("mic0_record", 44100, mic0_processed_signal)

    #pyroom stft
    # STFT = pra.transform.stft.STFT(N=2048)
    # stft_pra_sig0 = pra.transform.stft.analysis(mic0_processed_signal, L=2048, hop=128)
    # stft_pra_sig1 = pra.transform.stft.analysis(mic1_processed_signal, L=2048, hop=128)
    #######

    # STFT
    f1, t1, stft_signal1 = signal.stft(mic0_processed_signal, fs=sample_fs, nperseg=2048)
    f2, t2, stft_signal2 = signal.stft(mic1_processed_signal, fs=sample_fs, nperseg=2048)

    # DOA
    three_dim_sig1 = stft_signal1[np.newaxis, :]
    three_dim_sig2 = stft_signal2[np.newaxis, :]
    input_doa_signal = np.vstack([three_dim_sig1, three_dim_sig2])

    doa_module = doa_wrapper.DoaModuleWrapper(mic_location, room.fs, 2048,
                                              option=doa_wrapper.DoaModuleWrapper.DoaOption.MUSIC, src_count=src_count)
    doa_module.calculate_doa_and_plot(x_numpy_array=input_doa_signal, source_count=src_count)
    print("Calculated angle = " + str(doa_module.get_angle()))

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

    if master_plot: plt.show()

    return doa_module.get_angle()
