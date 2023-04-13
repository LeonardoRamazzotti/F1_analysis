# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 21:58:22 2023

@author: leona

Qualifying Laptime Telemetry for only 1 driver . No Comparisons

"""
import fastf1 as ff1
from fastf1 import plotting
from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
	

try:
	ff1.Cache.enable_cache('E:/My Drive/F1_Analysis/cache')
except:
    print('Cache not enable!')

# Setup plotting
plotting.setup_mpl()

#Input ========================================

year = 2023
gp = 'Bahrain'
driver= 'NOR'

#==============================================

quali_2022 = ff1.get_session(year,gp, "Q")


laps_22 = quali_2022.load_laps(with_telemetry=True)



lap_22 = laps_22.pick_driver(driver).pick_fastest()

tel_22 = lap_22.get_car_data().add_distance()



col = ff1.plotting.team_color(lap_22['Team'])
    


fig, ax = plt.subplots(5)
    
fig.suptitle(f"{year} {gp} {driver} Qualifiyng Lap")

ax[0].plot(tel_22['Distance'], tel_22['Speed'],color=col)
ax[0].set(ylabel='Speed')
ax[0].legend(loc="lower right")
ax[1].plot(tel_22['Distance'], tel_22['Throttle'],color=col)
ax[1].set(ylabel='Throttle')
ax[2].plot(tel_22['Distance'], tel_22['Brake'],color=col)
ax[2].set(ylabel='Brakes')
ax[3].plot(tel_22['Distance'], tel_22['RPM'],color=col)
ax[3].set(ylabel='RPM')
ax[4].plot(tel_22['Distance'], tel_22['nGear'],color=col)
ax[4].set(ylabel='GEAR')



for a in ax.flat:
        a.label_outer()
    
filesave=str(f"{year}_{gp}_qualifing_lap.png")

plt.savefig('graphics/'+filesave, dpi=1500)

plt.show()

