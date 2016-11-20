#!/usr/bin/env python3
#A program to plot the popularity of a phrase in a chat over time
#TODO: improve logic
import argparse
from json import loads
import datetime
from os import path
import matplotlib.pyplot as plt

dt = datetime.date
parser = argparse.ArgumentParser(description="Visualise the usage of a phrase in a chat over time")
parser.add_argument('filename', help='the json file (chat log) to analyse')
parser.add_argument('keyword', help='the keyword to search for')

args = parser.parse_args()
filename = args.filename
keyword = args.keyword

jsonfile = open(filename, 'r')

alldata = []
datesRaw = []
datesFrequency = []
#for line in jsonfile:
#    alldata.append(loads(line))

alldata = [loads(line) for line in jsonfile]

jsonfile.close()

for message in alldata:
    try:
        if keyword in message["text"]:
            #dates.append([message["date"], message["text"]])
            datesRaw.append(dt.fromtimestamp(message["date"]))
    except KeyError:
        pass

uniqDates = sorted(set(datesRaw))
for date in uniqDates:
    datesFrequency.append(datesRaw.count(date))
#plt.plot(counts)
plt.plot(uniqDates, datesFrequency)
plt.title("usage of \"{}\" in {}".format(keyword, path.split(filename)[-1][:-6])) #file name minus extension jsonl
#note that filename slicing is dependent on the extension being .jsonl
plt.show()
