import numpy as np

import room
#==================================================#
micLocation1 = np.array([[1.0, 1.0], [3.98, 4.02], [1.5, 1.5]])
micLocation2 = np.array([[3.02, 2.98], [1.5, 1.5], [1.5, 1.5]])

angleFromFirstPair = room.receiveAngles(micLocation1)
angleFromSecondPair = room.receiveAngles(micLocation2)

print(angleFromFirstPair)
print(360-angleFromSecondPair)