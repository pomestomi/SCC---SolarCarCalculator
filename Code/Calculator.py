# The Solar Car Calculator SCC is able to calculate the rentability of an electric camper van with solar cells on the rooftop compared to a conventional camper van using fossil fuels.
# It is expected that the electric camper is much more expensive, but cheaper in the upkeep since electricity is generated on the roof and maintenance is cheaper.
# The author thinks that the rentability mainly depends on the personal usage profile, e.g. the time and the amount of sunshine in his local area between drives. This calculator aims
# at answering this question with irradiation data from the German Weather Service DWD and google movement tracking that the author gathered in the last half year while driving his
# conventional camper van.
# @author: pomestomi


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

filename = 'Data/SolarData.txt'
data = np.loadtxt(filename, delimiter=';', dtype=str)
dataSelected = np.zeros((799,4))


plt.figure(0)
plt.plot(dataSelected[:,0],dataSelected[:,1],'y-')
plt.plot(dataSelected[:,0],dataSelected[:,2],'g-')
plt.plot(dataSelected[:,0],dataSelected[:,3],'b-')

plt.legend(['CH0, 18 uH','CH1, 18 uH','CH2, 4.7 uH'])
plt.title('Mit Zuleitungen')
plt.ylabel('Cap in pF') 
plt.xlabel('Temp in °C')
plt.grid(True)

