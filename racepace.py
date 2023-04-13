# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:31:40 2023

@author: leona

racepace comparison beetween seasons. Cut of 107% laps

"""
import fastf1 as ff1
from fastf1 import plotting

import pandas as pd

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import cm

import numpy as np

plotting.setup_mpl()

# Enable the cache
try:
    ff1.Cache.enable_cache('E:/My Drive/F1_Analysis/cache')
except:
    print('Cache not enable!')
# Get rid of some pandas warnings that are not relevant for us at the moment
pd.options.mode.chained_assignment = None 


#data input ========================
y1=2022
y2=2023
driver='HAM'
gp='Australia'
session='R'
#===================================

race1=ff1.get_session(y1,gp,session)
race2=ff1.get_session(y2,gp,session)

#===================================

laps1 = race1.load_laps(with_telemetry=True)
laps2 = race2.load_laps(with_telemetry=True)

#===================================

laps_past = laps1.pick_driver(driver)
laps_curr = laps2.pick_driver(driver)

#===================================

team = laps_past.pick_fastest()['Team']

#===================================

laps_past['RaceLapNumber'] = laps_past['LapNumber'] -1
laps_curr['RaceLapNumber'] = laps_curr['LapNumber'] -1

#===================================
# Eliminating too slow laps to avoid laps under safety car 
laps_past = laps_past.pick_quicklaps(1.07)
laps_curr = laps_curr.pick_quicklaps(1.07)

#===================================
# To get accurate laps only, we exclude in- and outlaps
laps_past = laps_past.loc[(laps_past['PitOutTime'].isnull() & laps_past['PitInTime'].isnull())]
laps_curr = laps_curr.loc[(laps_curr['PitOutTime'].isnull() & laps_curr['PitInTime'].isnull())]

#===================================
# Means
laps_past_mean=np.mean(laps_past['LapTime'])
laps_curr_mean=np.mean(laps_curr['LapTime'])

laps_past_mean = str(laps_past_mean)
laps_curr_mean = str(laps_curr_mean)

laps_past_mean = laps_past_mean.split(' ')
laps_curr_mean = laps_curr_mean.split(' ')

laps_past_mean = laps_past_mean[2]
laps_curr_mean = laps_curr_mean[2]

laps_past_mean = laps_past_mean.replace('00:','')
laps_curr_mean = laps_curr_mean.replace('00:','')

col = ff1.plotting.team_color(team)

plt.rcParams['figure.figsize'] = [10, 6]

fig, ax = plt.subplots()
fig.suptitle(f'{gp} Gp {y1} Vs {y2} {driver} RacePace')

ax.plot(laps_past['RaceLapNumber'], laps_past['LapTime'], label=(f'{driver} {y1}\n{laps_past_mean}'),color='#ffffff', linestyle=':')
ax.plot(laps_curr['RaceLapNumber'], laps_curr['LapTime'], label=(f'{driver} {y2}\n{laps_curr_mean}'),color=col)




ax.legend(loc="upper center")
ax.set_ylabel('LapTime')
ax.set_xlabel('Lap')

# Hide x labels and tick labels for top plots and y ticks for right plots.


plt.show()





