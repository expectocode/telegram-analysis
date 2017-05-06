#!/usr/bin/env python3
"""
A program to plot a pie chart of the most active users in a Telegram chat
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
    parser = argparse.ArgumentParser(description=
            "Create a pie chart showing the most active users in a Telegram chat")
    required = parser.add_argument_group('required arguments')
    parser.add_argument(
            '-o', '--output-folder',
            help='the folder to save the pie chart image in.'
            'Using this option will make the graph not display on screen.')
    required.add_argument('-f','--file',
            help='the jsonl chatlog file to analyse',
            required = True
            )
    parser.add_argument(
            '-s','--figure-size',
            help='the size of the figure shown or saved (X and Y size).'
            'Choose an appropriate value for your screen size. Default 12 8.',
            nargs=2,type=int
            )

    args = parser.parse_args()
    filepath = args.file
    savefolder = args.output_folder
    if args.figure_size is not None:
        figure_size = (args.figure_size[0],args.figure_size[1])
    else:
        figure_size = (12,8)

    _, filename = path.split(filepath)
    filename, _ = path.splitext(filename)
    #make filename just the name of the file, with no leading directories and no extension

    counter = defaultdict(int) #store events from each user
    names = {} #dict
    total_datapoints = 0

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            if "from" in event and "text" in event:#ugly but don't know better
                if "peer_id" in event["from"] and "print_name" in event["from"]:
                    total_datapoints += len(event["text"])
                    user = event["from"]["peer_id"]
                    #now make name for this ID the newest print name
                    names[str(user)] = event["from"]["print_name"]
                    if event["from"]["print_name"] == "":
                        names[str(user)] = event["from"]["peer_id"]
                    counter[user] += len(event["text"])

    trimmedCounter = defaultdict(int)

    #find percentile to start adding people to "other" at
    percentile = total_datapoints / 80 #anyone who contributes less than 1.125 percent of chars?

    for person, frequency in counter.items():
        if frequency < percentile:
            trimmedCounter["other"] += frequency
        else:
            trimmedCounter[names[str(person)]] = frequency

    sortedCounter = sorted(trimmedCounter.items(), key=itemgetter(1))
    print(sortedCounter)

    freqList = list(zip(*sortedCounter))

    plt.figure(figsize=figure_size)
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
