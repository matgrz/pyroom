import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.io import wavfile

import DoaModuleWrapper as doaWrapper
import RoomBuilder as roomBuild

# == data to plot ==
plotRir          = 1
plotRoom         = 1
plotSpectrogram1 = 1
plotSpectrogram2 = 1
# ==================

# prepare initial variables
soundFilePath = "src/female.wav"
sampleFs, voiceSample = wavfile.read(soundFilePath)
voiceSample = voiceSample[:180000]
absorptionFactor = 0.1
fs = 44100
# end of init variables

# prepare a room
floor = np.array([[0, 0, 6, 6],
                  [0, 8, 8, 0]])
micLocation = np.array([[5.0, 5.0], [3.96, 4.04], [1.5, 1.5]])

room = roomBuild.RoomBuilder(floor, fs, absorptionFactor, height=3.5, sourcesArray=[1, 4, 1.8],
                             filePath=soundFilePath, micLocationArray=micLocation).getRoom()

# source signal convolution
room.compute_rir()
mic1TimeSignal = np.convolve(voiceSample, room.rir[0][0])
mic2TimeSignal = np.convolve(voiceSample, room.rir[1][0])

# STFT
f1, t1, stftSignal1 = signal.stft(mic1TimeSignal, fs=sampleFs, nperseg=2048)
f2, t2, stftSignal2 = signal.stft(mic2TimeSignal, fs=sampleFs, nperseg=2048)

# DOA
threeDimSig1 = stftSignal1[np.newaxis, :]
threeDimSig2 = stftSignal2[np.newaxis, :]
print(np.shape(np.vstack([threeDimSig1, threeDimSig2])))

doaModule = doaWrapper.DoaModuleWrapper(micLocation, room.fs, 2048, option=doaWrapper.DoaModuleWrapper.DoaOption.SRP)
doaModule.calculateDoaAndPlot(xNumpyArray=np.vstack([threeDimSig1, threeDimSig2]), sourceCount=1)
print("Calculated angle = " + str(doaModule.getAngle()))

if plotSpectrogram1:
    plt.figure("Spectrogram1")
    plt.pcolormesh(t1, f1, np.abs(stftSignal1))

if plotSpectrogram2:
    plt.figure("Spectrogram2")
    plt.specgram(mic1TimeSignal, Fs=sampleFs)

if plotRoom:
    room.plot(img_order=1, aspect='equal')

if plotRir:
    plt.figure("rir")
    room.plot_rir()

plt.show()
