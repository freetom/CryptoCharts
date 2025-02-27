import matplotlib.pyplot as plt
import numpy as np
import json
from sys import argv
from datetime import datetime

def compute_MA_help(last_ndays):
    i = 0
    while i < len(last_ndays):
        i += 1

def compute_MA(history, ndays):
    last_ndays = [0] * ndays
    MA_x,MA_y = [], []
    i, j = len(history) - 1, 0
    start = history[len(history) - 1]['date']/1000
    daily_MA, daily_tick_counter = 0, 0
    while i >= 0:
        if start + 86400 < history[i]['date']/1000:
            daily_MA /= daily_tick_counter
            daily_tick_counter = 0
            last_ndays[j] = daily_MA
            j += 1
            if j >= ndays:
                j = 0
            MA_x.append(start*1000)
            ii, avg, jj =  0, 0, 0
            while ii < len(last_ndays):
                avg += last_ndays[ii]
                if last_ndays[ii] == 0:
                    jj += 1
                ii += 1
            avg /= ii - jj
            MA_y.append(avg)

            start = history[i]['date']/1000

        daily_MA += history[i]['rate']
        daily_tick_counter += 1
        i -= 1
    return (MA_x,MA_y)

xpoints = []
ypoints = []
with open('./history/'+argv[1], 'r') as f:
    history = json.loads(f.read().replace('\'','"'))
    history.sort(key=lambda d: d['date'], reverse=True)
    for h in history:
        xpoints.append(h['date'])
        ypoints.append(h['rate'])

plt.plot(xpoints, ypoints, label=argv[1].replace('_',''))
(x,y) = compute_MA(history, 30)
plt.plot(x, y, label='MA30')
(x,y) = compute_MA(history, 60)
plt.plot(x, y, label='MA60')
(x,y) = compute_MA(history, 120)
plt.plot(x, y, label='MA120')
(x,y) = compute_MA(history, 180)
plt.plot(x, y, label='MA180')

plt.legend()

xlocs, xlabs = plt.xticks()
i = 0
while i < len(xlocs):
    d = datetime.fromtimestamp(xlocs[i]/1000)
    formatted_date = str(d.month)+'/'+str(d.day)+'/'+str(d.year)+' \n'+str(d.hour)+':'+str(d.minute)
    xlabs[i] = formatted_date
    i += 1

plt.xticks(xlocs, xlabs)
plt.show()
