import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
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


class RoomWrapper:

    def __init__(self, config):
        self.config = config
        self.src_count = 1
        self.voice_sample_female = None
        self.voice_sample_male = None
        self.order = config.max_order

    def receive_angles(self, mic_location):

        room = self.create_room(mic_location, self.config.source_location1, self.config.source_location2, self.order)
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

        room = self.create_room(mic_location, self.config.source_location1, self.config.source_location2, self.order)
        room.simulate()
        processed_signals_array = self.process_signals(room.mic_array)
        _, _, input_doa_signal = self.calculate_stft(processed_signals_array)
        doa_module = self.create_doa_module(mic_location, room)
        wide_doa = self.create_doa_module(mic_location, room, doa_type=doa_wrapper.DoaModuleWrapper.DoaOption.SRP)

        fr_len = 5  # TODO remove hardcoded value and extract parameter
        fr_limit = 100

        list_of_frames_dicts = []   # contains [index_of_frame, dictionary for that frame, theta]

        # part I
        for frame_no in range(0, fr_limit, fr_len):     # dla kazdej ramki danej macierzy mikrofonowej np.shape(t1)[0]

            print("LOG_DBG: frame_no = ", frame_no)
            fi = dict.fromkeys(self.config.L)           # stworz slownik z kluczami dla L

            for l in self.config.L:                            # dla każdej czestotliwości l należacej do L
                fi[l] = doa_module.calculate_narrowband_doa(input_doa_signal[:, :, frame_no:(frame_no + fr_len)], l)      # wylicz DOA wąskopasmowo dla freq. bin = l dla ramki o długości fr_len * nsamples

                wide_doa.calculate_doa(input_doa_signal[:, :, frame_no:(frame_no + fr_len)])  # wylicz DOA szerokopasmowo     TODO zapytać o kąty - porównywać do "lokalnych" należących do ramki czy do finalnie wyznaczonych
            theta = doa_module.get_angle()                                                    # przypisz do danej ramki
            print("LOG_DBG: broadband doa angles = ", theta)

            index = frame_no / fr_len
            list_of_frames_dicts.append([index, fi, theta])
            print(fi)

        # part II # TODO prepare variant where alle angles have their feateures calculated
        feature_list1 = {}.fromkeys(self.config.L, 0)  # [freq, value] - dla danej czestotliwosci l przypisana liczba dopasowań
        feature_list2 = {}.fromkeys(self.config.L, 0)  # dla drugiego kąta

        frames_count = np.shape(list_of_frames_dicts)[0]
        print("LOG_DBG: frames estimations = ", list_of_frames_dicts)
        print("LOG_DBG: fr_count = ", frames_count)

        for frame_index in range(history_length - 1, frames_count):             # liczba_ramek - B porównań
            for tou_prim in range(frame_index - history_length, frame_index):   # zacznij od pierwszych B ramek, dla kazdej ramki tou_prim pomiedzy obecna ramka a B poprzednimi
                for l in self.config.L:  # dla kazdej freq l z L
                    index_theta = 2
                    index_dict = 1
                    first_angle = 0
                    second_angle = 1

                    left_operand = ((list_of_frames_dicts[tou_prim][index_dict])[l])[first_angle]        # TODO [first_angle]
                    theta_array = (list_of_frames_dicts[frame_index][index_theta])
                                                                                                            # TODO implement checking with previous frames, function input: current and B previous frames, output bool
                    if processing.calculate_angular_distance(left_operand, theta_array[first_angle]) \
                       < processing.calculate_angular_distance(left_operand, theta_array[second_angle]):    # TODO swap first/secnond_angle

                        if processing.calculate_angular_distance(left_operand, theta_array[first_angle]) < threshold:   # TODO [first_angle]
                            feature_list1[l] += 1
                                                                                                            # dla drugiego kąta
                    if processing.calculate_angular_distance(left_operand, theta_array[second_angle]) \
                        < processing.calculate_angular_distance(left_operand, theta_array[first_angle]):

                        if processing.calculate_angular_distance(left_operand, theta_array[second_angle]) < threshold:
                            feature_list2[l] += 1

        print("LOG_DBG: feature list = ", feature_list1)
        return feature_list1, feature_list2

    def create_doa_module(self, mic_location, room, doa_type=doa_wrapper.DoaModuleWrapper.DoaOption.MUSIC):
        doa_module = doa_wrapper.DoaModuleWrapper(mic_location, room.fs, self.config.nsamples, src_count=self.src_count,
                                                  option=doa_type)
        return doa_module

    def create_room(self, mic_location, source1, source2, max_order=0):
        self.read_signals()
        builder = room_builder.RoomBuilder(self.config.room_dimension, self.config.fs,
                                           absorption_factor=self.config.absorption, mic_location_array=mic_location,
                                           order=max_order)
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
