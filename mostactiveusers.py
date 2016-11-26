#!/usr/bin/env python3
"""
A program to plot the most active users in a telegram chat, given a log
"""
import argparse
from json import loads
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt
from operator import itemgetter

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(description="analyse a json output of a telegram backup utility")
    parser.add_argument(
            '-o', '--output-folder',
            help='output the figure to image file in this folder')
    parser.add_argument('filepath', help='the json file to analyse')

    args = parser.parse_args()
    filepath = args.filepath
    savefolder = args.output_folder

    _, filename = path.split(filepath)
    filename, _ = path.splitext(filename)
    #make filename just the name of the file, with no leading directories and no extension

    counter = defaultdict(int) #store events from each user
    total_datapoints = 0

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            if "from" and "text" in event:#ugly but don't know better
                if "username" in event["from"]:
                    total_datapoints += len(event["text"])
                    user = event["from"]["username"]
                    counter[user] += len(event["text"])

    trimmedCounter = defaultdict(int)

    #find percentile to start adding people to "other" at
    percentile = total_datapoints / 80 #anyone who contributes less than 1.125 percent of chars?

    for person, frequency in counter.items():
        if frequency < percentile: # <3
            trimmedCounter["other"] += frequency
        else:
            trimmedCounter[person] = frequency

    sortedCounter = sorted(trimmedCounter.items(), key=itemgetter(1))
    print(sortedCounter)

    freqList = list(zip(*sortedCounter))

    plt.figure(figsize=(12,8))
    plt.title("Most active users in {} by chars sent".format(filename), y=1.05)
    plt.pie(freqList[1], labels=freqList[0], startangle=135)
#    plt.set_lw(10)
    plt.axis('equal')
    #so it plots as a circle

    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        plt.savefig("{}/Most active users in {}.png".format(savefolder, filename))
    else:
    #if a save folder was not specified, just open a window to display graph
        plt.show()

#    print(type(*sorted(counter.items())))
 #   plt.pie(*zip(*sorted(counter.items())))

if __name__ == "__main__":
    main()
