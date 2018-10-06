import pyroomacoustics as pra
from scipy.io import wavfile
import numpy as np


class RoomBuilder:
    def __init__(self, floor, fs, absorption_factor, height, sources_array, file_path, mic_location_array):

        self.room = pra.Room.from_corners(floor, fs=fs, absorption=absorption_factor, max_order=0)

        self.set_height(height)
        # self.add_sources(sources_array, voice_sample)
        self.add_microphones(mic_location_array)

        # signal = [voiceSample, voiceSample]  # must have valid format after .shape
        # self.room.mic_array.record(np.asanyarray(signal), sampleFs)

    def set_height(self, height):
        self.room.extrude(height=height)

    def add_sources(self, sources_array, voice_sample):
        sound_source = pra.soundsource.SoundSource(sources_array, signal=voice_sample)
        self.room.add_source(sound_source.position, signal=sound_source.signal)

    def add_microphones(self, mic_location_array):
        mic_array = pra.MicrophoneArray(mic_location_array, self.room.fs)
        self.room.add_microphone_array(mic_array)

    def get_room(self):
        return self.room
