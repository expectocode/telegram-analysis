#!/usr/bin/env python3
"""
A program to plot the activity in a chat over time
"""
import argparse
from json import loads
from datetime import date,timedelta
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Visualise and compare the activity of one or more Telegram chats over time.")
    required = parser.add_argument_group('required arguments')
    #https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
    required.add_argument(
            '-f', '--files',
            help='paths to the json file(s) (chat logs) to analyse.',
            required = True,
            nargs='+'
            )
    parser.add_argument(
            '-o', '--output-folder',
            help='the foler to save the activity graph image in.'
            'Using this option will make the graph not display on screen.')
    parser.add_argument(
            '-b', '--bin-size',
            help='the number of days to group together as one datapoint. Higher number is more smooth graph, lower number is more spiky. Default 3')
            #and negative bin sizes are = 1

    args = parser.parse_args()
    filepaths = args.files
    savefolder = args.output_folder
    if args.bin_size is not None:
        binsize = int(args.bin_size)
    else:
        binsize = 3

    filenames = []
    plt.figure(figsize=(14,8))
    #make a decent default size.

    for filepath in filepaths:
        with open(filepath, 'r') as jsonfile:
            events = (loads(line) for line in jsonfile)
            #generator, so whole file is not put in mem
            counter = defaultdict(int)
            #a dict with dates as keys and frequency as values
            if binsize > 1:
                #this makes binsizes ! > 1 act as 1
                for ind,event in enumerate(events):
                    if ind==0 or (curbin - date.fromtimestamp(event['date']) > timedelta(days=binsize)):
                        curbin=date.fromtimestamp(event['date'])
                    if "text" in event:
                        counter[curbin] += len(event["text"])
            else:
                for event in events:
                    if "text" in event:
                        day = date.fromtimestamp(event["date"])
                        counter[day] += len(event["text"])

        #if binsize > 1:
        #    #this makes binsizes which are 1 or less act as if they are 1 (ie no binning)
        #    l = sorted(counter.items())
        #    binnedcounter = defaultdict(int)
        #    curbin = l[0][0]
        #    for tup in l:
        #        if tup[0] - curbin > timedelta(days=binsize):
        #            curbin = tup[0]
        #        binnedcounter[curbin] += tup[1]
        #else:
        #    binnedcounter = counter

        _, temp = path.split(filepath)
        filenames.append(temp)
        filenames[filepaths.index(filepath)] , _ = path.splitext(
                filenames[filepaths.index(filepath)] )
        #make filename just the name of the file,
        # with no leading directories and no extension

        frequencies = sorted(counter.items())
        #find frequency of chat events per date

        plt.plot(*zip(*frequencies))
        plt.grid()
        #because i think it looks better with the grid

    #end for

    if len(filenames) > 1:
        plt.title("Activity in {}".format(filenames))
        plt.legend(filenames, loc='best')
    else:
        plt.title("Activity in {}".format(filenames[0]))

    plt.ylabel("Activity level (chars per day)", size=14)

    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        chats_string = ""
        for chat in filenames:
            chats_string+=chat
            chats_string+="_"

        if len(chats_string) > 200:
        #file name likely to be so long as to cause issues
            figname = input(
                "This graph is going to have a very long file name. Please enter a custom name(no need to add an extension): ")
        else:
            figname = "Activity in {}".format(chats_string)

        plt.savefig("{}/{}.png".format(savefolder, figname))
    else:
        #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
