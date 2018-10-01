import pyroomacoustics as pra
from scipy.io import wavfile
import numpy as np

class RoomBuilder:
    def __init__(self, floor, fs, absorptionFactor, height, sourcesArray, filePath, micLocationArray):
        sampleFs, voiceSample = wavfile.read(filePath)
        voiceSample = voiceSample[:180000]

        self.room = pra.Room.from_corners(floor, fs=fs, max_order=12, absorption=absorptionFactor)

        self.setHeight(height)
        self.addSources(sourcesArray, voiceSample)
        self.addMicrophones(micLocationArray)

        signal = [voiceSample, voiceSample]  # must have valid format after .shape
        self.room.mic_array.record(np.asanyarray(signal), sampleFs)

    def setHeight(self, height):
        self.room.extrude(height=height)

    def addSources(self, sourcesArray, voiceSample):
        soundSource = pra.soundsource.SoundSource(sourcesArray, signal=voiceSample)
        self.room.add_source(soundSource.position, signal=soundSource.signal)

    def addMicrophones(self, micLocationArray):
        micArray = pra.MicrophoneArray(micLocationArray, self.room.fs)
        self.room.add_microphone_array(micArray)

    def getRoom(self):
        return self.room