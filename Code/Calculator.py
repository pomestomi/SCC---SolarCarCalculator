# The Solar Car Calculator SCC is able to calculate the rentability of an electric camper van with solar cells on the rooftop compared to a conventional camper van using fossil fuels.
# It is expected that the electric camper is much more expensive, but cheaper in the upkeep since electricity is generated on the roof and maintenance is cheaper.
# The author thinks that the rentability mainly depends on the personal usage profile, e.g. the time and the amount of sunshine in his local area between drives. This calculator aims
# at answering this question with irradiation data from the German Weather Service DWD and google movement tracking that the author gathered in the last half year while driving his
# conventional camper van.
# @author: pomestomi


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Fiat Ducato L2H2 car with fossil fuel engine
initCostFossil = 45000
yearlyTaxCostFossil = 280
yearlyMaintenanceFossil = 245 # 75 + 120 + 50 for Oil, Maintenance in general, License 

yearlyCostsPerHourFossil = (yearlyTaxCostFossil + yearlyMaintenanceFossil)/(360*24)
fuelConsFossil = 10 # l/100km
fuelPriceFossil = 1.8 # Euro/l
fuelCostFossil = fuelConsFossil*fuelPriceFossil/100 # Euro/km

# Fiat Ducato L2H2 car with electric engine
initCostElectric = 66500 + 700 + 1300 + 3000 + 1000 # Car costs, Growatt SPF3500 ES 3,5kW + Pylontech US2000 C 2.5kWh + 10 Victron BlueSolar Solarmodul Polykristallin 330Wp + Extras
energyStorageSize = 79 # kWh
solarEfficiency = 0.2*1.1*0.95*0.95 # percent times difference between flat surface and angled surface and twice the charging losses of 5%, https://echtsolar.de/photovoltaik-neigungswinkel/
solarSurface = 10*2*1 # m^2
yearlyTaxCostElectric = (0*7 + 280*8)/15 # Electric cars are free of tax until 2030 in Germany. Afterwards we assume the same costs and average over 15 years
yearlyMaintenanceElectric = 100
yearlyBenefitElectric = -300 # THG Quota (selling Co2 certificates to oil companies)

yearlyCostsPerHourElectric = (yearlyTaxCostElectric + yearlyMaintenanceElectric + yearlyBenefitElectric)/(360*24)
fuelConsElectric = 33 # kWh/100km
fuelPriceElectric = 0.4 # Euro/kWh
fuelCostElectric = fuelConsElectric*fuelPriceElectric/100 #Euro/km



filename = './Code/Data/SolarData.txt'
data = np.genfromtxt(filename, delimiter=';', dtype=str)

filename = './Code/Data/DrivingDistances.txt'
dataDistance = np.genfromtxt(filename, delimiter='\t', dtype=str)

#extract relevant time range from weather data
startDate = '2022-06-16-00:00'
startTimestamp= int(datetime.timestamp(datetime.strptime(startDate, '%Y-%m-%d-%H:%M')))

#allocate data array that will contain weather and consumption data. The array will contain:
# Timestamp | SolarPower | FossilCosts | ElectricCosts | StorageLevel
dataSelected = np.zeros([np.size(dataDistance,0),5])

#write init costs in first row
dataSelected[0,2] = initCostFossil
dataSelected[0,3] = initCostElectric
dataSelected[0,4] = 0 #Start with empty energy storage

n = 1   
i = 1
totalPower = 0
while n < np.size(data,0):
    if (int(datetime.timestamp(datetime.strptime(data[n,1], '%Y%m%d%H:%M')))) > startTimestamp:
        dataSelected[i,0] = int(datetime.timestamp(datetime.strptime(data[n,1], '%Y%m%d%H:%M')))
        dataSelected[i,1] = float(data[n,5])*0.00278 # convert from J/cm2 to kwh/m2

        # Add hourly expenses
        dataSelected[i,2] = dataSelected[i-1,2] + yearlyCostsPerHourFossil
        dataSelected[i,3] = dataSelected[i-1,3] + yearlyCostsPerHourElectric

        # Calculate fuel costs fossil car
        dataSelected[i,2] = dataSelected[i,2] + int(dataDistance[i,1])*fuelCostFossil

        # Calculate fuel costs solar
        # First, if the car was not moved, add generated energy to storage. Crop the storage to max capacity
        if (int(dataDistance[i,1]) == 0):
            dataSelected[i,4] = dataSelected[i-1,4] + dataSelected[i,1]*solarSurface*solarEfficiency
            if dataSelected[i,4] > energyStorageSize:
                dataSelected[i,4] = energyStorageSize

        # If the car was moved, calculate the energy needed
        if (int(dataDistance[i,1]) != 0):
            energyConsumed = int(dataDistance[i,1])/100*fuelConsElectric
            # Reduce energy storage by this amount
            dataSelected[i,4] = dataSelected[i-1,4] - energyConsumed
            # If more energy is needed than available, add that to the running costs
            if dataSelected[i,4] < 0:
                dataSelected[i,3] = dataSelected[i,3] + -1*dataSelected[i,4]*fuelPriceElectric
                # And reset storage to 0
                dataSelected[i,4] = 0
        # TOODOO: Add the energy production with reduced surface while driving



        totalPower = totalPower + dataSelected[i,1]
        i = i+1
    n = n+1


print('Total Power: ' + str(totalPower/1000) + ' kWh/m2')


plt.figure()
plt.plot(6.5+(dataSelected[:,0]-startTimestamp)/(60*60*24*30),dataSelected[:,1],'r-')

plt.title('Global Irradiation')
plt.legend(['Solar Irradiation Nürnberg 2022'])
plt.ylabel('Wh/m2') 
plt.xlabel('Month')
plt.xlim([6,12])
plt.grid(True)
plt.show()


plt.figure()
plt.plot(6.5+(dataSelected[:,0]-startTimestamp)/(60*60*24*30),dataSelected[:,4],'r-')

plt.title('Battery level')
plt.legend(['Battery level if charged'])
plt.ylabel('kWh') 
plt.xlabel('Month')
plt.xlim([6,12])
plt.grid(True)
plt.show()


plt.figure()
plt.plot(6.5+(dataSelected[:,0]-startTimestamp)/(60*60*24*30),dataSelected[:,2],'r-')
plt.plot(6.5+(dataSelected[:,0]-startTimestamp)/(60*60*24*30),dataSelected[:,3]-27500,'g-')

plt.title('Vehicle cost')
plt.legend(['Diesel', 'Electric'])
plt.ylabel('Euro') 
plt.xlabel('Month')
plt.xlim([6,12])
plt.grid(True)
plt.show()




