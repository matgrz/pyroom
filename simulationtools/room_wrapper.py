import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile

from simulationtools import room_builder as room_builder, doa_module_wrapper as doa_wrapper
from utils import processing
from utils import log

log = log.Log()


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
        log.INFO("Calculated angle = " + str(doa_module.get_angle()))

        if self.config.plot_doa_radar:
            doa_module.plot_doa()

        if self.config.plot_spectrogram1:
            plt.figure("Spectrogram1")
            plt.pcolormesh(t1, f1, np.abs(input_doa_signal[0, :, :]))

        if self.config.plot_spectrogram2:
            plt.figure("Spectrogram2")
            plt.specgram(processed_signals_array[0], Fs=self.config.fs)
            plt.xlabel("czas [s]", fontsize=12)
            plt.ylabel("częstotliwość [Hz]", fontsize=12)

        if self.config.plot_room:
            room.plot(img_order=1, aspect='equal')
            plt.xlabel("x axis")
            plt.ylabel("y axis")

        if self.config.plot_rir:
            plt.figure("rir")
            room.plot_rir()

        if self.config.master_plot:
            plt.show()

        if self.config.write_mic_signal:
            wavfile.write("mic0_record", 44100, processed_signals_array[0])

        return doa_module.get_angle()

    def receive_features(self, mic_location, doas):

        history_length = self.config.history_length
        threshold = self.config.threshold
        fr_limit = self.config.frame_limit

        room = self.create_room(mic_location, self.config.source_location1, self.config.source_location2, self.order)
        room.simulate()
        processed_signals_array = self.process_signals(room.mic_array)
        _, _, input_doa_signal = self.calculate_stft(processed_signals_array)
        doa_module = self.create_doa_module(mic_location, room)

        list_of_frames_dicts = []   # contains [index_of_frame, dictionary for that frame, theta]

        # part I
        for frame_no in range(0, fr_limit):

            # log.DBG("frame_no = ", frame_no)
            fi = dict.fromkeys(self.config.L)        # create dict with keys for every l

            for l in self.config.L:   # TODO find different way to calculate DOA for single freq - this one is very time consuming
                fi[l] = doa_module.calculate_narrowband_doa(input_doa_signal[:, :, frame_no:(frame_no + 1)], l)

            list_of_frames_dicts.append([frame_no, fi])
            # log.DBG("fi value: ", fi)

        frames_count = np.shape(list_of_frames_dicts)[0]
        # log.DBG("frames estimations = ", list_of_frames_dicts)
        # log.DBG("fr_count = ", frames_count)

        all_feature_lists = list()
        for frame_index in range(history_length - 1, frames_count, history_length):
            feature_list1 = {}.fromkeys(self.config.L, 0)  # [freq, value]-value means how many times freq was associated
            feature_list2 = {}.fromkeys(self.config.L, 0)
            for tou_prim in range(frame_index - history_length, frame_index):
                for l in self.config.L:
                    index_dict = 1

                    k = threshold
                    hist_index = 0

                    for teta_p in doas:
                        # log.DBG("theta_p = ", teta_p)
                        for fi_tou in (list_of_frames_dicts[tou_prim][index_dict])[l]:
                            # log.DBG("    fi_tou = ", fi_tou)
                            # log.DBG("    A = ", processing.calculate_angular_distance(fi_tou, teta_p))
                            if processing.calculate_angular_distance(fi_tou, teta_p) < k:
                                k = processing.calculate_angular_distance(fi_tou, teta_p)
                                hist_index = teta_p

                    if k < threshold:
                        if hist_index == doas[0]:
                            # log.DBG("    assigned to 1")
                            feature_list1[l] += 1
                        elif hist_index == doas[1]:
                            # log.DBG("    assigned to 2")
                            feature_list2[l] += 1

            all_feature_lists.append([feature_list1, feature_list2])

        return all_feature_lists

    def create_doa_module(self, mic_location, room, doa_type=doa_wrapper.DoaModuleWrapper.DoaOption.MUSIC):
        doa_module = doa_wrapper.DoaModuleWrapper(mic_location, room.fs, self.config.nsamples, src_count=self.src_count,
                                                  option=doa_type)
        return doa_module

    def create_room(self, mic_location, source1, source2, max_order=0):
        self.read_signals()
        builder = room_builder.RoomBuilder(self.config.room_dimension, self.config.fs,
                                           absorption_factor=self.config.absorption, mic_location_array=mic_location,
                                           order=max_order)
        builder.add_sources(sources_array=source1, voice_sample=self.voice_sample_female, delay=0.0)
        room = builder.get_room()

        if source2 is not None:
            self.src_count = 2
            room.add_source(position=source2, signal=self.voice_sample_male)

        return room

    def read_signals(self):
        sound_file_path_female = self.config.src_signal1
        _, voice_sample_female = wavfile.read(sound_file_path_female)
        self.voice_sample_female = voice_sample_female[:120000]
        sound_file_path_male = self.config.src_signal2
        _, voice_sample_male = wavfile.read(sound_file_path_male)
        self.voice_sample_male = voice_sample_male[40000:160000]

    def process_signals(self, rooms_mic_array):
        mic_processed_signals = []

        for mic_index in range(np.shape(rooms_mic_array.signals)[0]):
            mic_processed_signals.append(processing.convert_float_signal_to_int(rooms_mic_array.signals[mic_index, :]))

        return mic_processed_signals

    def calculate_stft(self, processed_signals_array):
        """
        Calculates stft for every microphone in the array. Vstack adds another dimension which represents
        microphone count.
        :param processed_signals_array: array with processed microphone signals
        :return: output of single stft as two vectors: f and t, inpud DOA signal
        """
        stft_signals = []
        f_list, t_list = [], []
        for stft_index in range(np.shape(processed_signals_array)[0]):
            f_list, t_list, temp_sig = signal.stft(processed_signals_array[stft_index], fs=self.config.fs,
                                                   nperseg=self.config.nsamples)
            stft_signals.append(temp_sig[np.newaxis, :])

        return f_list, t_list, np.vstack(stft_signals)
