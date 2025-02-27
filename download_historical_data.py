# !/bin/python3
# Downloads a crypto's historical price,marketcap,volume data from livecoinwatch
# Saves it by updating/creating the coin's history file (with an ordered JSON array)

from sys import argv
from history import query_asset_history
from datetime import datetime
import json
import requests
from time import sleep
from math import ceil
import os.path

if len(argv) != 4:
    print('usage: '+argv[0]+' symbol start_date end_date')
    print('example: '+argv[0]+' ADA 2020-01 2021-01')
    print('example: '+argv[0]+' ADA 2020-01-13 2021-01-16')
    exit(1)

now = datetime.now().timestamp()
print('Epoch Now: ' +str(bin(int(now)))[2:])

if len(argv[2].split('-')) == 2:
    start = datetime(int(argv[2].split('-')[0]), int(argv[2].split('-')[1]), 1)
else:
    start = datetime(int(argv[2].split('-')[0]), int(argv[2].split('-')[1]), int(argv[2].split('-')[2]))
if len(argv[3].split('-')) == 2:
    end = datetime(int(argv[3].split('-')[0]), int(argv[3].split('-')[1]), 1)
else:
    end = datetime(int(argv[3].split('-')[0]), int(argv[3].split('-')[1]), int(argv[3].split('-')[2]))

if now < start.timestamp(): # or now < end.timestamp():
    print('Invalid future dates')
    exit(1)

print('Coin:\t'+str(argv[1]))
print('Start date:\t'+str(start))
print('End date:\t'+str(end))

print()
print('Loading existing coin history')
full_history, full_history_d = [], {}
if os.path.isfile('./history/'+argv[1]):
    with open('./history/'+argv[1], 'r') as f:
        full_history = json.loads(f.read())
        for block in full_history:
            full_history_d[block['date']] = block


start_t = int(start.timestamp())*1000
end_t = int(end.timestamp())*1000
n, tot = 0, str(int(ceil((end_t-start_t)/86400000)))
while start_t < end_t:
    if start_t > now * 1000:
        print('date in the future, skipping')
        start_t += 86400000
        continue
    history = json.loads(query_asset_history(argv[1],start_t,start_t+86400000))
    history['history'].sort(key=lambda d: d['date'], reverse=False)
    if history['history'][0]['date'] in full_history_d and history['history'][len(history)-1]['date'] in full_history_d:
        print('data already there skipping..')
    else:
        full_history += history['history']
    #print(len(history['history']))
    n += 1
    print('Downloaded '+str(n)+'/'+tot+'\r', end='')
    start_t += 86400000
    sleep(11.3)	# to not get blocked
#print()
print('Updating coin history file...')
full_history.sort(key=lambda d: d['date'], reverse=False)
f = open('./history/'+argv[1], 'w')
json.dump(full_history, f)
