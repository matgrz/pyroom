import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import pyroomacoustics as pra
from scipy.io import wavfile

import DoaModuleWrapper as doaWrapper
import RoomBuilder as roomBuild

# == data to plot ==
masterPlot       = 1
plotRir          = 0
plotRoom         = 1
plotSpectrogram1 = 0
plotSpectrogram2 = 0
# ==================
def receiveAngles(micLocation):
    # prepare initial variables
    soundFilePath = "src/female.wav"
    sampleFs, voiceSample = wavfile.read(soundFilePath)
    voiceSample = voiceSample[:180000]
    absorptionFactor = 0.3
    fs = 44100
    # end of init variables

    # prepare a room
    floor = np.array([[0, 0, 6, 6],
                      [0, 8, 8, 0]])
    # micLocation = np.array([[1.0, 1.0], [3.98, 4.02], [1.5, 1.5]])
    # micLocation1 = np.array([[3.02, 2.98], [1.5, 1.5], [1.5, 1.5]])

    room = roomBuild.RoomBuilder(floor, fs, absorptionFactor, height=3.5, sourcesArray=[2.6, 4.7, 1.8],
                                 filePath=soundFilePath, micLocationArray=micLocation).getRoom()
    micArray = pra.MicrophoneArray(micLocation, room.fs)
    room.add_microphone_array(micArray)

    # source signal convolution
    room.compute_rir()
    room.simulate(True)

    print("conv shape: ", np.shape(room.mic_array))

    mic1TimeSignal = np.convolve(voiceSample, room.rir[0][0])
    mic2TimeSignal = np.convolve(voiceSample, room.rir[1][0])

    # STFT
    f1, t1, stftSignal1 = signal.stft(mic1TimeSignal, fs=sampleFs, nperseg=2048)
    f2, t2, stftSignal2 = signal.stft(mic2TimeSignal, fs=sampleFs, nperseg=2048)

    # DOA
    threeDimSig1 = stftSignal1[np.newaxis, :]
    threeDimSig2 = stftSignal2[np.newaxis, :]
    print(np.shape(stftSignal1))
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
        plt.xlabel("x axis")
        plt.ylabel("y axis")

    if plotRir:
        plt.figure("rir")
        room.plot_rir()

    if masterPlot: plt.show()

    return doaModule.getAngle()
