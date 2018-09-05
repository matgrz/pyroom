import numpy as np
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.io import wavfile

# prepare initial variables
soundFilePath = "src/sample.wav"
sampleFs, voiceSample = wavfile.read(soundFilePath)
absorptionFactor = 0.1
fs = 48000
micsPositions = [[3.0], [1.0], [1.5]]

# prepare a room
floor = np.array([[0, 0, 6, 6],
                  [0, 8, 8, 0]])
room = pra.Room.from_corners(floor, fs=fs, max_order=12, absorption=absorptionFactor)
room.extrude(3.5, absorption=absorptionFactor)

# add a source
soundSource = pra.soundsource.SoundSource([3, 6, 1.8], signal=voiceSample)
room.add_source(soundSource.position, signal=soundSource.signal)

# add microphones
array = np.array([[3.0], [1.0], [1.5]])
micArray = pra.MicrophoneArray(array, room.fs)
room.add_microphone_array(micArray)

room.mic_array.record(voiceSample, sampleFs)

# DOA
# stftTransfromer = pra.transform.stft.STFT(2048, 1)
# doa = pra.doa.SRP(array, room.fs, 2048)
# doa.locate_sources()


# training things
# bf = pra.Beamformer(micsPositions, sampleFs)
#rirArr = pra.soundsource.build_rir_matrix(room.mic_array, room.sources, 8, room.fs)
# rirSource = room.sources[0].get_rir(room.mic_array, 1, room.fs)


# end of training things

# room.image_source_model()
room.plot(img_order=1, aspect='equal')

room.simulate()
# room.plot_rir()
plt.show()

