
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:31:40 2023

@author: leona

Qualifycation event gap beetween all the drivers.

"""
import matplotlib.pyplot as plt
import pandas as pd 
from timple.timedelta import strftimedelta
import fastf1 as ff1
import fastf1.plotting
from fastf1.core import Laps

try:
    ff1.Cache.enable_cache('E:/My Drive/F1_Analysis/cache')
except:
    print('Cache not enable!')
# INPUT ==========================================
year = 2023
gp = 'Australia'


fastf1.plotting.setup_mpl(mpl_timedelta_support=True, color_scheme=None, misc_mpl_mods=False)

session = fastf1.get_session(year,gp, 'Q')
session.load()

drivers = pd.unique(session.laps['Driver'])
print(drivers)

list_fastest_laps = list()
for drv in drivers:
    drvs_fastest_lap = session.laps.pick_driver(drv).pick_fastest()
    list_fastest_laps.append(drvs_fastest_lap)
fastest_laps = Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

pole_lap = fastest_laps.pick_fastest()
fastest_laps['LapTimeDelta'] = fastest_laps['LapTime'] - pole_lap['LapTime']

print(fastest_laps[['Driver', 'LapTime', 'LapTimeDelta']])

team_colors = list()
for index, lap in fastest_laps.iterlaps():
    color = fastf1.plotting.team_color(index['Team'])
    team_colors.append(color)

fig, ax = plt.subplots()
ax.barh(fastest_laps.index, fastest_laps['LapTimeDelta'],
        color=team_colors, edgecolor='grey')
ax.set_yticks(fastest_laps.index)
ax.set_yticklabels(fastest_laps['Driver'])

# show fastest at the top
ax.invert_yaxis()

# draw vertical lines behind the bars
ax.set_axisbelow(True)
ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)


lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')

plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
             f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")

plt.savefig(f"{session.event['EventName']}_{session.event.year}_quali_gap.png", dpi=1500)
plt.show()