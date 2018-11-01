from enum import Enum
import pyroomacoustics as pra


class DoaModuleWrapper:
    class DoaOption(Enum):
        SRP = 0
        MUSIC = 1

    def __init__(self, mic_position_array, room_frequency_sample, nfft, src_count, option=DoaOption.SRP):
        if option == self.DoaOption.SRP:
            self.doaModule = pra.doa.SRP(mic_position_array, room_frequency_sample, nfft, num_src=src_count)
        else:
            self.doaModule = pra.doa.MUSIC(mic_position_array, room_frequency_sample, nfft, num_src=src_count)

    def calculate_doa(self, x_numpy_array):
        self.doaModule.locate_sources(x_numpy_array, freq_range=[500, 2000])

    def calculate_narrowband_doa(self, x_numpy_array, l):
        self.doaModule.locate_sources(x_numpy_array, freq_bins=[l])
        return self.doaModule.src_idx

    def plot_doa(self):
        self.doaModule.polar_plt_dirac()

    def get_angle(self):
        return self.doaModule.src_idx
