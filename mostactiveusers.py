#!/usr/bin/env python3
"""
A program to plot a pie chart of the most active users in a Telegram chat
"""
import argparse
from json import loads
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import date,datetime
from operator import itemgetter

def parse_args():
    parser = argparse.ArgumentParser(description=
            "Create a pie chart showing the most active users in a Telegram chat")
    required = parser.add_argument_group('required arguments')
    required.add_argument('-f','--file',
            help='the jsonl chatlog file to analyse',
            required = True
            )
    parser.add_argument(
            '-o', '--output-folder',
            help='the folder to save the pie chart image in.'
            'Using this option will make the graph not display on screen.')
    parser.add_argument(
            '-s','--figure-size',
            help='the size of the figure shown or saved (X and Y size).'
            'Choose an appropriate value for your screen size. Default 12 8.',
            nargs=2,type=int,default = [12,8]
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

def get_dates(arg_dates):
    if " " not in arg_dates:
        print("You must put a space between start and end dates")
        exit()
    daterange = arg_dates.split()
    start_date = datetime.strptime(daterange[0], "%Y-%m-%d").date()
    end_date = datetime.strptime(daterange[1], "%Y-%m-%d").date()
    return (start_date,end_date)

def extract_infos(event):
    text_date = date.fromtimestamp(event['date'])
    text_length = len(event['text'])
    text_userid= event['from']['peer_id']
    text_printname = event['from']['print_name']
    return text_date,text_length,text_userid,text_printname

def make_ddict(jsonfile,start,end):
    """
    Make a defaultdict with user IDs as keys and char count as values
    Return (dict of IDs -> names, total chars, defaultdict)
    """
    names = {} #dict
    counter = defaultdict(int)
    total_datapoints = 0
    events = (loads(line) for line in jsonfile)
    messages = (extract_infos(event) for event in events if 'text' in event)
    messages = ((when,what,uid,who) for (when,what,uid,who) in messages if when > start and when < end)
    for (msgdate,textlength,userid,printname) in messages:
        total_datapoints += textlength
        if str(userid) not in names:
            #this code assumes that chatlog has most recent events first
            #which is default for telegram-history-dumper
            names[str(userid)] = printname
        if printname == "":
            names[str(userid)] = str(userid)
        counter[userid] += textlength

    return names,total_datapoints,counter

def annotate_figure(filename):
    plt.title("Most active users in {} by chars sent".format(filename), y=1.05)
    plt.axis('equal')
    #so it plots as a circle

def make_trimmed_ddict(counter,total_datapoints,names,min_percent):
    trimmedCounter = defaultdict(int)
    #find percentile to start adding people to "other" at
    min_chars = (min_percent/100) * total_datapoints
    for person, frequency in counter.items():
        if frequency < min_chars:
            trimmedCounter["other"] += frequency
        else:
            if names[str(person)] == "other":
                print("Someone in this chat is called 'other'. "
                "They will be absorbed into the 'other' pie slice.")
            trimmedCounter[names[str(person)]] = frequency

    return trimmedCounter

def main():
    """
    main function
    """

    args = parse_args()
    filepath = args.file
    savefolder = args.output_folder
    figure_size = (args.figure_size[0],args.figure_size[1])
    start_date,end_date = get_dates(args.date_range)
    other_percent = 2
    #anyone who sends less than this percentage of the total is 'other'

    filename = path.splitext(path.split(filepath)[-1])[0]
    #make filename just the name of the file, with no leading directories and no extension

    with open(filepath, 'r') as jsonfile:
        names,total_datapoints,counter = make_ddict(jsonfile,start_date,end_date)

    trimmedCounter = make_trimmed_ddict(counter,total_datapoints,names,other_percent)

    sortedCounter = sorted(trimmedCounter.items(), key=itemgetter(1))
    print(sortedCounter)

    freqList = list(zip(*sortedCounter))
    plt.figure(figsize=figure_size)

    plt.pie(freqList[1], labels=freqList[0], startangle=135)
    annotate_figure(filename)
#    plt.set_lw(10)

    if savefolder is not None:
        #if there is a given folder to save the figure in, save it there
        plt.savefig("{}/Most active users in {}.png".format(savefolder, filename))
    else:
        #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
