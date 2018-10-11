import pyroomacoustics as pra
from scipy.io import wavfile
import numpy as np


class RoomBuilder:
    def __init__(self, room_dimensions, fs, absorption_factor, mic_location_array):

        # self.room = pra.Room.from_corners(floor, fs=fs, absorption=absorption_factor, max_order=1)
        self.room = pra.ShoeBox(room_dimensions, fs=fs, absorption=absorption_factor, max_order=3)

        self.add_microphones(mic_location_array, fs)

    def set_height(self, height):
        self.room.extrude(height=height)

    def add_sources(self, sources_array, voice_sample, delay=0.0):
        self.room.add_source(sources_array, signal=voice_sample, delay=delay)

    def add_microphones(self, mic_location_array, fs):
        mic_array = pra.MicrophoneArray(mic_location_array, fs)
        self.room.add_microphone_array(mic_array)

    def get_room(self):
        return self.room
