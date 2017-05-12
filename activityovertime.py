#!/usr/bin/env python3
"""
A program to plot the activity in a chat over time
"""
import argparse
from json import loads
from datetime import date,timedelta,datetime
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt

def make_ddict(json_file,binsize):
    """
    return a defaultdict(int) of dates with activity on those dates
    """
    events = (loads(line) for line in json_file)
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

    return counter

def make_ddict_in_date_range(json_file,binsize,start_stamp,end_stamp):
    """
    return a defaultdict(int) of dates with activity on those dates
    """
    events = (loads(line) for line in json_file)
    #generator, so whole file is not put in mem
    counter = defaultdict(int)
    #a dict with dates as keys and frequency as values
    if binsize > 1:
        #this makes binsizes ! > 1 act as 1
        curbin = 0
        for ind,event in enumerate(events):
            if int(event['date']) > start_stamp and int(event['date']) < end_stamp:
                if curbin==0 or (curbin - date.fromtimestamp(event['date']) > timedelta(days=binsize)):
                    curbin=date.fromtimestamp(event['date'])
                if "text" in event:
                    counter[curbin] += len(event["text"])
    else:
        for event in events:
            if int(event['date']) > start_date and int(event['date']) < end_date:
                if "text" in event:
                    day = date.fromtimestamp(event["date"])
                    counter[day] += len(event["text"])

    return counter

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
            help='the folder to save the activity graph image in.'
            'Using this option will make the graph not display on screen.')
    parser.add_argument(
            '-b', '--bin-size',
            help='the number of days to group together as one datapoint. Higher number is more smooth graph, lower number is more spiky. Default 3')
            #and negative bin sizes are = 1
    parser.add_argument(
            '-s','--figure-size',
            help='the size of the figure shown or saved (X and Y size).'
            'Choose an appropriate value for your screen size. Default 14 8.',
            nargs=2,type=int
            )
    parser.add_argument(
            '-d','--date-range',
            help='the range of dates you want to look at data between. '
            'Must be in format YYYY-MM-DD YYYY-MM-DD with the first date '
            'the start of the range, and the second the end. Example: '
            '-d "2017-11-20 2017-05-15". Make sure you don\'t put a day '
            'that is too high for the month eg 30th February.'
    )

    args = parser.parse_args()

    filepaths = args.files
    savefolder = args.output_folder
    if args.bin_size is not None:
        binsize = int(args.bin_size)
    else:
        binsize = 3
    if args.figure_size is not None:
        figure_size = (args.figure_size[0],args.figure_size[1])
    else:
        figure_size = (14,8)
    if args.date_range is not None:
        if " " not in args.date_range:
            print("Invalid date range")
            exit()
        daterange = args.date_range.split()
        #using strftime('%s') is not portable. not great practice.
        start_date = int(datetime.strptime(daterange[0], "%Y-%m-%d").strftime('%s'))
        end_date = int(datetime.strptime(daterange[1], "%Y-%m-%d").strftime('%s'))

    filenames = []
    plt.figure(figsize=figure_size)
    #make a decent default size.

    for filepath in filepaths:
        with open(filepath, 'r') as jsonfile:
            if args.date_range is not None:
                counter = make_ddict_in_date_range(
                        jsonfile,binsize,start_date,end_date)
            else:
                counter = make_ddict(jsonfile,binsize)

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
        chats_string = '_'.join(filenames)

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
