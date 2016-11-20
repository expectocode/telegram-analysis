#!/usr/bin/env python3
#A program to plot the popularity of a phrase in a chat over time
#TODO: improve logic
import argparse
from json import loads
from datetime import date
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(
        description="Visualise the usage of a phrase in a chat over time")
parser.add_argument('filename', help='the json file (chat log) to analyse')
parser.add_argument('keyword', help='the keyword to search for')

args = parser.parse_args()
filename = args.filename
keyword = args.keyword

with open(filename, 'r') as jsonfile:
    events = (loads(line) for line in jsonfile)

    counter = defaultdict(int)
    for event in events:
        if "text" in event and keyword in event["text"]:
            day = date.fromtimestamp(event["date"])
            counter[day] += 1

frequencies = sorted(counter.items())
plt.plot(*zip(*frequencies))
plt.title("usage of \"{}\" in {}".format(keyword, path.split(filename)[-1][:-6])) #file name minus extension jsonl
#note that filename slicing is dependent on the extension being .jsonl
plt.show()
