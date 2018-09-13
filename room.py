import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.io import wavfile

# prepare initial variables
soundFilePath = "src/female.wav"
sampleFs, voiceSample = wavfile.read(soundFilePath)
voiceSample = voiceSample[:180000]
absorptionFactor = 0.1
fs = 44100
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
array = np.array([[2.96, 3.04], [1.0, 1.0], [1.5, 1.5]])
micArray = pra.MicrophoneArray(array, room.fs)
room.add_microphone_array(micArray)

    # record signals
sig = [voiceSample, voiceSample]     # must have valid format after .shape
room.mic_array.record(np.asanyarray(sig), sampleFs)

# source signal convolution
room.compute_rir()
mic1TimeSignal = np.convolve(voiceSample, room.rir[0][0])
mic2TimeSignal = np.convolve(voiceSample, room.rir[1][0])

# STFT
f1, t1, stftSignal1 = signal.stft(mic1TimeSignal, fs=sampleFs, nperseg=2048)
f2, t2, stftSignal2 = signal.stft(mic2TimeSignal, fs=sampleFs, nperseg=2048)

# DOA
# stftTransfromer = pra.transform.stft.STFT(2048, 1)
threeDimSig1 = stftSignal1[np.newaxis, :]
threeDimSig2 = stftSignal2[np.newaxis, :]
print(np.shape(np.vstack([threeDimSig1, threeDimSig2])))

doaModule = pra.doa.SRP(array, room.fs, 2048)
doaModule.locate_sources(np.vstack([threeDimSig1, threeDimSig2]), num_src=1)
doaModule.polar_plt_dirac()
print(doaModule.src_idx)

plt.pcolormesh(t1, f1, np.abs(stftSignal1))
# plt.specgram(mic1TimeSignal, Fs=sampleFs)

# training things

# end of training things

# room.image_source_model()
room.plot(img_order=1, aspect='equal')

# room.plot_rir()
plt.show()

