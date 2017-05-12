#!/usr/bin/env python3
"""
A program to plot the popularity of a phrase in a chat over time
"""
import argparse
from json import loads
from datetime import date,datetime,timedelta
from os import path
from collections import defaultdict
import matplotlib.pyplot as plt

def make_word_counters(jsonfile, keywords,binsize,case_sensitive):
    """
    return a list of defaultdict(list) of phrases over time.
    Each phrase has a dict of True/False lists for each day or bin.
    """
    events = (loads(line) for line in jsonfile)
    #generator, so whole file is not put in mem
    word_counters = [defaultdict(list) for keyword in keywords]

    if binsize > 1:
        curbin = 0
        for ind,event in enumerate(events):
            #if int(event['date']) > start_date and int(event['date']) < end_date:
            if curbin == 0 or (
                    curbin - date.fromtimestamp(event['date']) > timedelta(days=binsize)):
                curbin=date.fromtimestamp(event['date'])
            if "text" in event:
                for k_ind,keyword in enumerate(keywords):
                    if case_sensitive:
                    #case sens or insens search for the keyword
                        word_counters[k_ind][curbin].append(keyword in event["text"])
                    else:
                        word_counters[k_ind][curbin].append(
                            "text" in event and keyword in event["text"].lower())
    else:
        for event in events:
            if "text" in event:
                for k_ind,keyword in enumerate(keywords):
                    if args.case_sensitive:
                    #case sens or insens search for the keyword
                        day = date.fromtimestamp(event["date"])
                        word_counters[k_ind][day].append(keyword in event["text"])
                    else:
                        day = date.fromtimestamp(event["date"])
                        word_counters[k_ind][day].append(keyword in event["text"].lower())
    return word_counters

def make_word_counters_in_date_range(jsonfile, keywords,binsize,case_sensitive,d_start,d_end):
    """
    return a list of defaultdict(list) of phrases over time, in a specified date range.
    Each phrase has a dict of True/False lists for each day or bin.
    Date range specified with unix timestamps.
    """
    events = (loads(line) for line in jsonfile)
    #generator, so whole file is not put in mem
    word_counters = [defaultdict(list) for keyword in keywords]

    if binsize > 1:
        curbin = 0
        for ind,event in enumerate(events):
            #if int(event['date']) > start_date and int(event['date']) < end_date:
            if int(event['date']) > d_start and int(event['date']) < d_end:
                if curbin == 0 or (
                        curbin - date.fromtimestamp(event['date']) > timedelta(days=binsize)):
                    curbin=date.fromtimestamp(event['date'])
                if "text" in event:
                    for k_ind,keyword in enumerate(keywords):
                        if case_sensitive:
                        #case sens or insens search for the keyword
                            word_counters[k_ind][curbin].append(keyword in event["text"])
                        else:
                            word_counters[k_ind][curbin].append(
                                "text" in event and keyword in event["text"].lower())
    else:
        for event in events:
            if int(event['date']) > d_start and int(event['date']) < d_end:
                if "text" in event:
                    for k_ind,keyword in enumerate(keywords):
                        if args.case_sensitive:
                        #case sens or insens search for the keyword
                            day = date.fromtimestamp(event["date"])
                            word_counters[k_ind][day].append(keyword in event["text"])
                        else:
                            day = date.fromtimestamp(event["date"])
                            word_counters[k_ind][day].append(keyword in event["text"].lower())
    return word_counters

def parse_args():
    parser = argparse.ArgumentParser(
            description="Visualise and compare the usage of one or more words/phrases in a chat over time")
    required = parser.add_argument_group('required arguments')
    parser.add_argument('-c', '--case-sensitive',
            help='make the phrase search case sensitive',
            action='store_true')
    parser.add_argument('-o', '--output-folder',
            help='the folder to save the graph image in')
    parser.add_argument('-b', '--bin-size',
            help='the number of days to group together as one datapoint. Higher number is more smooth graph, lower number is more spiky. Default 3')
    required.add_argument('-f','--file',
            help='path to the json file (chat log) to analyse')
    required.add_argument('-p','--phrases',
            help='the phrase(s) to search for',
            nargs='+',
            required = True)
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
            "-d '2017-11-20 2017-05-15'. Make sure you don't put a day "
            'that is too high for the month eg 30th February.'
    )
    return parser.parse_args()

def draw_figure(word_counters,keywords,figure_size):
    frequenciesList = []
    plt.figure(figsize=figure_size)
    for x in range(len(keywords)):
    #make a frequencies thing for each keyword, and plot each one onto the plot
        frequenciesList.append(
        {key: l.count(True)/len(l) * 100 for key, l in word_counters[x].items()})
        #find frequency of keyword use per date
        plt.plot(*zip(*sorted(frequenciesList[x].items())))

    plt.grid()
    #because i think it looks better with the grid

def annotate_figure(filename,keywords,case_sensitive):
    if case_sensitive:
    #pretty self explanatory. this is added to the title.
        postfix=", case sensitive"
    else:
        postfix=", case insensitive"
    if len(keywords) > 1:
        plt.title(
            "usage of {} in {}{}".format(keywords, filename, postfix))
        plt.legend(keywords)
    else:
        plt.title(
            'usage of "{}" in {}{}'.format(keywords[0], filename, postfix))
        #plt.legend(keywords[0])

#    plt.ylabel("Percentage of messages containing \"{}\"".format(keyword), size=14)
    plt.ylabel("Percentage of messages containing keywords", size=14)

def save_figure(folder,filename,keywords):
    keywords_string = '_'.join(keywords)
    if len(keywords_string) > 200:
    #file name likely to be so long as to cause issues
        figname = input(
            "This graph is going to have a very long file name. Please enter a custom name(no need to add an extension): ")
    else:
        figname = "{} in {}".format(
            keywords_string, filename)

    plt.savefig("{}/{}.png".format(folder, figname))

def main():
    """
    main function
    """

    args = parse_args()
    filepath = args.file
    keywords = args.phrases
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
            print("You must put a space between the start and end dates")
            exit()
        daterange = args.date_range.split()
        #using strftime('%s') is not portable. not great practice.
        start_date = int(datetime.strptime(daterange[0], "%Y-%m-%d").strftime('%s'))
        end_date = int(datetime.strptime(daterange[1], "%Y-%m-%d").strftime('%s'))

    with open(filepath, 'r') as jsonfile:
        if args.date_range is not None:
            word_counters = make_word_counters_in_date_range(
                    jsonfile,keywords,binsize,args.case_sensitive,start_date,end_date)
        else:
            word_counters = make_word_counters(jsonfile,keywords,binsize,args.case_sensitive)

    filename = path.splitext(path.split(filepath)[-1])[0]
    #make filename just the name of the file,
    # with no leading directories and no extension

    draw_figure(word_counters,keywords,figure_size)
    annotate_figure(filename,keywords,args.case_sensitive)

    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        save_figure(savefolder,filename,keywords)
    else:
    #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
