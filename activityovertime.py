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
from sys import maxsize

def extract_date_and_len(event):
       text_date = date.fromtimestamp(event['date'])
       text_length = len(event['text'])
       return text_date, text_length

def make_ddict_in_range(json_file,binsize,start,end):
    """
    return a defaultdict(int) of dates with activity on those dates in a date range
    """
    events = (loads(line) for line in json_file)
    #generator, so whole file is not put in mem
    dates_and_lengths = (extract_date_and_len(event) for event in events if 'text' in event)
    dates_and_lengths = ((date,length) for (date,length) in dates_and_lengths if date > start and date < end)
    counter = defaultdict(int)
    #a dict with dates as keys and frequency as values
    if binsize > 1:
        #this makes binsizes ! > 1 act as 1
        curbin = 0
        for date_text,length in dates_and_lengths:
            if curbin == 0 or (curbin - date_text) > timedelta(days=binsize):
                curbin = date_text
            counter[curbin] += length
    else:
        for date_text,length in dates_and_lengths:
            counter[date_text] += length

    return counter

def parse_args():
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
            help='the number of days to group together as one datapoint. '
            'Higher number is more smooth graph, lower number is more spiky. '
            'Default 3.',
            type=int,default=3)
            #and negative bin sizes are = 1
    parser.add_argument(
            '-s','--figure-size',
            help='the size of the figure shown or saved (X and Y size).'
            'Choose an appropriate value for your screen size. Default 14 8.',
            nargs=2,type=int,default=[14,8]
            )
    parser.add_argument(
            '-d','--date-range',
            help='the range of dates you want to look at data between. '
            'Must be in format YYYY-MM-DD YYYY-MM-DD with the first date '
            'the start of the range, and the second the end. Example: '
            "-d '2017-11-20 2017-05-15'. Make sure you don't put a day "
            'that is too high for the month eg 30th February.',
            default="1000-01-01 4017-01-01"
            #hopefully no chatlogs contain these dates :p
    )

    return parser.parse_args()

def save_figure(folder,filenames):
    chats_string = '_'.join(filenames)

    if len(chats_string) > 200:
    #file name likely to be so long as to cause issues
        figname = input(
            "This graph is going to have a very long file name. Please enter a custom name(no need to add an extension): ")
    else:
        figname = "Activity in {}".format(chats_string)

    plt.savefig("{}/{}.png".format(folder, figname))

def annotate_figure(filenames,binsize):
    if len(filenames) > 1:
        plt.title("Activity in {}".format(filenames))
        plt.legend(filenames, loc='best')
    else:
        plt.title("Activity in {}".format(filenames[0]))

    if binsize > 1:
        plt.ylabel("Activity level (chars per {} days)".format(binsize), size=14)
    else:
        plt.ylabel("Activity level (chars per day)", size=14)

def get_dates(arg_dates):
    if " " not in arg_dates:
        print("You must put a space between start and end dates")
        exit()
    daterange = arg_dates.split()
    start_date = datetime.strptime(daterange[0], "%Y-%m-%d").date()
    end_date = datetime.strptime(daterange[1], "%Y-%m-%d").date()
    return (start_date,end_date)

def main():
    """
    main function
    """

    args = parse_args()

    #set up args
    filepaths = args.files
    savefolder = args.output_folder
    binsize = args.bin_size
    figure_size = args.figure_size
    start_date,end_date = get_dates(args.date_range)

    filenames = []

    plt.figure(figsize=figure_size)

    for ind,filepath in enumerate(filepaths):
        with open(filepath, 'r') as jsonfile:
            #if args.date_range is not None:
            #    chat_counter = make_ddict_in_date_range(
            #            jsonfile,binsize,start_date,end_date)
            #else:
            #    chat_counter = make_ddict(jsonfile,binsize)
            chat_counter = make_ddict_in_range(
                    jsonfile,binsize,start_date,end_date)

        filenames.append(path.splitext(path.split(filepath)[-1])[0])
        #make filename just the name of the file,
        # with no leading directories and no extension

        chat_activity = sorted(chat_counter.items())
        #find frequency of chat events per date

        plt.plot(*zip(*chat_activity))
        plt.grid()
        #because i think it looks better with the grid

    annotate_figure(filenames,binsize)

    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        save_figure(savefolder,filenames)
    else:
        #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
