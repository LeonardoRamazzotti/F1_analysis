# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:31:40 2023

@author: leona

Scatter that compare for every driver TopSpeed and Laptime due to evaluate the type of circuit 
and the setup. 

"""

import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd
from pandas import datetime, Timedelta

try:
    ff1.Cache.enable_cache('E:/My Drive/F1_Analysis/cache')
except:
    print('Cache not enable!')

plotting.setup_mpl()

# DATA IMPUT ==================================
year = 2023
gp = 'Australia'
session='Q'
#==============================================

race=ff1.get_session(year,gp,session)

laps = race.load_laps(with_telemetry = True)

driver_list=list(pd.unique(race.laps['Driver']))




list_laptime = []
list_speed = []
'''
team_colors = []
for index in driver_list :
    driver = laps.pick_driver(index).pick_fastest()
    color = ff1.plotting.team_color(driver['Team'])
    team_colors.append(color)
'''


plt.rcParams['figure.figsize'] = [10, 6]

fig, ax = plt.subplots()

fig.suptitle(f'{gp} Qualifying {year}')

for driver in driver_list:
    lap = laps.pick_driver(driver).pick_fastest()
    elemet=lap['LapTime'].strftime('%M:%S.%f')
    ax.plot(lap['SpeedST'],lap['LapTime'], marker='o', markersize = 15, label= driver)

# Hide x labels and tick labels for top plots and y ticks for right plots.
for a in ax.flat:
    a.label_outer()
   

ax.legend(loc="upper center")    
ax.set(ylabel='LapTime')
ax.set(xlabel='Top Speed (km/h)')