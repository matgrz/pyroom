import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

from simulationtools import room_builder as room_builder, doa_module_wrapper as doa_wrapper
from utils import processing
from .config import baseconfig

# == data to plot ==
master_plot       = 0
plot_rir          = 0
plot_room         = 0
plot_doa_radar    = 0
plot_spectrogram1 = 0
plot_spectrogram2 = 0
# ==================


class RoomWrapper:

    def __init__(self):
        self.config = baseconfig.BaseConfig()
        self.src_count = 1
        self.voice_sample_female = None
        self.voice_sample_male = None

    def receive_angles(self, mic_location, source1, source2=None):

        room = self.create_room(mic_location, source1, source2)
        room.simulate()
        processed_signals_array = self.process_signals(room.mic_array)
        f1, t1, input_doa_signal = self.calculate_stft(processed_signals_array)
        doa_module = self.create_doa_module(mic_location, room)
        doa_module.calculate_doa(x_numpy_array=input_doa_signal)
        print("LOG_INFO: Calculated angle = " + str(doa_module.get_angle()))

        if plot_doa_radar:
            doa_module.plot_doa()

        # if plot_spectrogram1:
        #     plt.figure("Spectrogram1")
        #     plt.pcolormesh(t1, f1, np.abs(stft_signal1))
        #
        # if plot_spectrogram2:
        #     plt.figure("Spectrogram2")
        #     plt.specgram(mic0_processed_signal, Fs=self.config.fs)

        if plot_room:
            room.plot(img_order=1, aspect='equal')
            plt.xlabel("x axis")
            plt.ylabel("y axis")

        if plot_rir:
            plt.figure("rir")
            room.plot_rir()

        if master_plot:
            plt.show()
        wavfile.write("mic0_record", 44100, processed_signals_array[0])

        return doa_module.get_angle()

    def receive_features(self, mic_location, history_length, threshold):

        room = self.create_room(mic_location, self.config.source_location1, self.config.source_location2)
        room.simulate()
        processed_signals_array = self.process_signals(room.mic_array)
        f1, t1, input_doa_signal = self.calculate_stft(processed_signals_array)
        doa_module = self.create_doa_module(mic_location, room)

        fr_len = 5  # TODO remove hardcoded value and extract parameter
        fr_limit = 100

        list_of_frames_dicts = []   # contains [index_of_frame, dictionary for that frame, theta]

        # part I
        for frame_no in range(0, fr_limit, fr_len):     # dla kazdej ramki danej macierzy mikrofonowej np.shape(t1)[0]-5

            print("LOG_DBG: frame_no = ", frame_no)
            fi = dict.fromkeys(self.config.L)       # stworz slownik z kluczami dla L

            for l in self.config.L:                            # dla każdej czestotliwości l należacej do L
                print("LOG_DBG: l = ", l)
                fi[l] = [doa_module.calculate_narrowband_doa(input_doa_signal[:, :, frame_no:(frame_no + fr_len)], l)]      # wylicz DOA wąskopasmowo dla freq. bin = l dla ramki o długości fr_len * nsamples

            doa_module.calculate_doa(input_doa_signal[:, :, frame_no:(frame_no + fr_len)])  # wylicz DOA szerokopasmowo     TODO zapytać o kąty - porównywać do "lokalnych" należących do ramki czy do finalnie wyznaczonych
            theta = doa_module.get_angle()                                                  # przypisz do danej ramki
            print("LOG_DBG: broadband doa angles = ", theta)

            index = frame_no / fr_len
            list_of_frames_dicts.append([index, fi, theta])
            print(fi)

        # part II # TODO prepare variant where alle angles have their feateures calculated
        feature_list = {}.fromkeys(self.config.L, 0)  # [freq, value] - dla danej czestotliwosci l przypisana liczba dopasowań

        print("LOG_DBG: frames estimations = ", list_of_frames_dicts)
        frames_count = np.shape(list_of_frames_dicts)[0]
        print("LOG_DBG: fr_count = ", frames_count)

        for x in range(history_length - 1, frames_count):             # liczba_ramek - B porównań
            for tou_prim in range(history_length - 1, fr_limit // fr_len):   # zacznij od pierwszych B ramek, dla kazdej ramki tou_prim pomiedzy obecna ramka a B poprzednimi

                list_of_k = []  # lista wartosci zwracanych przez funkcjie angular distance - potem wyciagnac z tego min
                for l in self.config.L:  # dla kazdej freq l z L
                    # print("LOG_DBG: val from frames = ", ((list_of_frames_dicts[x][1])[l])[0][0])
                    # print("LOG_DBG: val from frames = ", (list_of_frames_dicts[x][2])[0])

                    # for angle in (list_of_frames_dicts[x][2]):
                    #     list_of_k.append(processing.calculate_angular_distance(((list_of_frames_dicts[x][1])[l])[0][0],     # jako argument z x'owej ramki wez slownik, a z jego l'tej czestotliwosci wez kąt
                    #                                                             angle))
                    # k = min(list_of_k)
                    # print("LOG_DBG: k = ", k)

                    if processing.calculate_angular_distance(((list_of_frames_dicts[x][1])[l])[0][0], (list_of_frames_dicts[x][2])[0]) < processing.calculate_angular_distance(((list_of_frames_dicts[x][1])[l])[0][0], (list_of_frames_dicts[x][2])[1]):

                        if processing.calculate_angular_distance(((list_of_frames_dicts[x][1])[l])[0][0], (list_of_frames_dicts[x][2])[0]) < threshold:
                            feature_list[l] += 1

        print("LOG_DBG: feature list = ", feature_list)
        return feature_list

    def create_doa_module(self, mic_location, room):
        doa_module = doa_wrapper.DoaModuleWrapper(mic_location, room.fs, self.config.nsamples, src_count=self.src_count,
                                                  option=doa_wrapper.DoaModuleWrapper.DoaOption.MUSIC)
        return doa_module

    def create_room(self, mic_location, source1, source2):
        self.read_signals()
        builder = room_builder.RoomBuilder(self.config.room_dimension, self.config.fs,
                                           absorption_factor=self.config.absorption, mic_location_array=mic_location)
        builder.add_sources(sources_array=source1, voice_sample=self.voice_sample_female, delay=0.2)
        room = builder.get_room()

        if source2 is not None:
            self.src_count = 2
            room.add_source(position=source2, signal=self.voice_sample_male)

        return room

    def read_signals(self):
        sound_file_path_female = "src/female.wav"
        _, voice_sample_female = wavfile.read(sound_file_path_female)
        self.voice_sample_female = voice_sample_female[:120000]
        sound_file_path_male = "src/male_fr.wav"
        _, voice_sample_male = wavfile.read(sound_file_path_male)
        self.voice_sample_male = voice_sample_male[40000:160000]

    def process_signals(self, rooms_mic_array):
        mic0_processed_signal = processing.convert_float_signal_to_int(rooms_mic_array.signals[0, :])
        mic1_processed_signal = processing.convert_float_signal_to_int(rooms_mic_array.signals[1, :])
        mic2_processed_signal = processing.convert_float_signal_to_int(rooms_mic_array.signals[2, :])
        mic3_processed_signal = processing.convert_float_signal_to_int(rooms_mic_array.signals[3, :])

        return [mic0_processed_signal, mic1_processed_signal, mic2_processed_signal, mic3_processed_signal]

    def calculate_stft(self, processed_signals_array):

        f1, t1, stft_signal1 = signal.stft(processed_signals_array[0], fs=self.config.fs, nperseg=self.config.nsamples)
        _, _, stft_signal2 = signal.stft(processed_signals_array[1], fs=self.config.fs, nperseg=self.config.nsamples)
        _, _, stft_signal3 = signal.stft(processed_signals_array[2], fs=self.config.fs, nperseg=self.config.nsamples)
        _, _, stft_signal4 = signal.stft(processed_signals_array[3], fs=self.config.fs, nperseg=self.config.nsamples)

        return f1, t1, np.vstack([stft_signal1[np.newaxis, :], stft_signal2[np.newaxis, :],
                                  stft_signal3[np.newaxis, :], stft_signal4[np.newaxis, :]])
