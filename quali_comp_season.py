# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 22:58:27 2023

@author: leona

Comparing Qualifying Laps beetween seasons . 

ADV. Only driver with the same Team has been compared
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
gp='Bahrain'

race1=ff1.get_session(y1,gp,'Q')
race2=ff1.get_session(y2,gp,'Q')

#===================================

laps1 = race1.load_laps(with_telemetry=True)
laps2 = race2.load_laps(with_telemetry=True)

laps1['LapTimeSeconds'] = laps1['LapTime'].dt.total_seconds()
laps2['LapTimeSeconds'] = laps2['LapTime'].dt.total_seconds()

print(laps1)

driver_list_1=list(pd.unique(race1.laps['Driver']))
driver_list_2=list(pd.unique(race2.laps['Driver']))

list_driver = []
list_delta = []

#commentare l'algoritmo
for driver1 in driver_list_1:
    print(driver1)
    team = laps1.pick_driver(driver1).pick_fastest()
    print(team['Team'])
    
    if driver1 in driver_list_2:
        team2 = laps2.pick_driver(driver1).pick_fastest()

        
        if str(team['Team']) == str(team2['Team']):
            delta = float(team2['LapTimeSeconds']) - float(team['LapTimeSeconds'])
            
            if delta < 10.00 and delta > -10.00:
                list_driver.append(driver1)
                list_delta.append(delta)
            

#s_dict_delta = sorted(dict_delta.values())

team_colors = []
for index in list_driver :
    driver = laps1.pick_driver(index).pick_fastest()
    color = ff1.plotting.team_color(driver['Team'])
    team_colors.append(color)

fig, ax = plt.subplots()
#ax = fig.add_axes([0,0,1,1])

ax.barh(list_driver,list_delta, color = team_colors, edgecolor='grey',animated = True)
# show fastest at the top
ax.invert_yaxis()
# draw vertical lines behind the bars
ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
ax.set(xlabel=f"Delta {y2}-{y1} (s)")



plt.suptitle(f"{race1.event['EventName']} Qualifying delta {y2} - {y1}")


plt.savefig(f"graphics/{gp}_Qualy_delta_{y2}_{y1}.png", dpi=1500)
plt.show()
		