#!/usr/bin/env python3
#A program to plot the popularity of a phrase in a chat over time
#TODO: improve logic
import argparse
from json import loads
import matplotlib.pyplot as plt
import datetime

dt=datetime.date
parser = argparse.ArgumentParser(description="Visualise the usage of a phrase in a chat over time")
parser.add_argument('filename', help='the json file (chat log) to analyse')
parser.add_argument('keyword', help='the keyword to search for')

args=parser.parse_args()
filename=args.filename
keyword=args.keyword

file = open(filename, 'r')

alldata=[]
datesRaw=[]
datesFrequency=[]
#messages
for line in file.readlines():
    alldata.append(loads(line))

for message in alldata:
    try:
        if keyword in message["text"]:
            #dates.append([message["date"], message["text"]])
            datesRaw.append(dt.fromtimestamp(message["date"]))
    except Exception:
        pass

uniqDates = sorted(set(datesRaw))
for date in uniqDates:
    datesFrequency.append(datesRaw.count(date))
#plt.plot(counts)
plt.plot(uniqDates, datesFrequency)
plt.title("usage of \"" + keyword + "\" in " + filename[5:-6])
#note that filename slicing is entirely dependent on your dir structure. this is for me. likely source of problems for other users.
plt.show()
