from enum import Enum
import pyroomacoustics as pra

class DoaModuleWrapper:
    class DoaOption(Enum):
        SRP = 0
        MUSIC = 1

    def __init__(self, micPositionArray, roomFrequencySample, nfft, option=DoaOption.SRP):
        if option == self.DoaOption.SRP:
            self.doaModule = pra.doa.SRP(micPositionArray, roomFrequencySample, nfft)
        else:
            self.doaModule = pra.doa.MUSIC(micPositionArray, roomFrequencySample, nfft)

    def calculateDoaAndPlot(self, xNumpyArray, sourceCount):
        self.doaModule.locate_sources(xNumpyArray, sourceCount)
        self.doaModule.polar_plt_dirac()

    def getAngle(self):
        return self.doaModule.src_idx
