#!/usr/bin/env python3
"""
A program to plot the popularity of a phrase in a chat over time
"""
import argparse
from json import loads
from datetime import date
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Visualise the activity of a chat over time")
    parser.add_argument('-o', '--output-folder', help='output the figure to image file in this folder')
    parser.add_argument('filepaths', help='paths to the json file(s) (chat logs) to analyse. Note these must be at the end of the arguments.', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    filepaths = args.filepaths
    savefolder = args.output_folder

    filenames = []
    plt.figure(figsize=(14,8)) #make a decent default size.

    for filepath in filepaths:
        with open(filepath, 'r') as jsonfile:
            events = (loads(line) for line in jsonfile) #generator, so whole file is not put in mem
            counter = defaultdict(int)  #a dict with dates as keys and frequency as values
            for event in events:
                day = date.fromtimestamp(event["date"])
                counter[day] += 1

        _, temp = path.split(filepath)
        filenames.append(temp)
        filenames[filepaths.index(filepath)] , _ = path.splitext(filenames[filepaths.index(filepath)] )
    #make filename just the name of the file, with no leading directories and no extension

        frequencies = sorted(counter.items()) #find frequency of chat events per date
        plt.plot(*zip(*frequencies))
        plt.grid() #because i think it looks better with the grid

    #end for

    plt.title("Activity in {}".format(filenames))
    plt.legend(filenames)
    plt.ylabel("Activity level (events per day)", size=14)

    if savefolder is not None: #if there is a given folder to save the figure in, save it there
        chats_string = ""
        for chat in filenames:
            chats_string+=chat
            chats_string+="_"
        plt.savefig("{}/activity_in_{}.png".format(savefolder, chats_string))
    else: #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
