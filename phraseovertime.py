#!/usr/bin/env python3
"""
A program to plot the popularity of a phrase in a chat over time
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
            description="Visualise and compare the usage of one or more words/phrases in a chat over time")
    required = parser.add_argument_group('required arguments')
    parser.add_argument('-c', '--case-sensitive',
            help='make the phrase search case sensitive',
            action='store_true')
    parser.add_argument('-o', '--output-folder',
            help='output the figure to image file in this folder')
    parser.add_argument('-b', '--bin-size',
            help='the number of days to group together as one datapoint. Higher number is more smooth graph, lower number is more spiky. Default 3')
    required.add_argument('-f','--file',
            help='path to the json file (chat log) to analyse')
    required.add_argument('-k','--keywords',
            help='the keyword(s) to search for',
            nargs='+',
            required = True)

    args = parser.parse_args()
    filepath = args.file
    keywords = args.keywords
    savefolder = args.output_folder
    if args.bin_size is not None:
        binsize = int(args.bin_size)
    else:
        binsize = 3

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        #generator, so whole file is not put in mem
        counters = [defaultdict(list) for keyword in keywords]

        if binsize > 1:
            for ind,event in enumerate(events):
                if ind==0 or (curbin - date.fromtimestamp(event['date']) > timedelta(days=binsize)):
                    curbin=date.fromtimestamp(event['date'])
                if "text" in event:
                    for keyword in keywords:
                        if args.case_sensitive:
                        #case sens or insens search for the keyword
                            counters[keywords.index(keyword)][curbin].append(
                                "text" in event and keyword in event["text"])
                        else:
                            counters[keywords.index(keyword)][curbin].append(
                                "text" in event and keyword in event["text"].lower())
        else:
            for event in events:
                if "text" in event:
                    for keyword in keywords:
                        if args.case_sensitive:
                        #case sens or insens search for the keyword
                            day = date.fromtimestamp(event["date"])
                            counters[keywords.index(keyword)][day].append(
                                "text" in event and keyword in event["text"])
                        else:
                            day = date.fromtimestamp(event["date"])
                            counters[keywords.index(keyword)][day].append(
                                "text" in event and keyword in event["text"].lower())

    _, filename = path.split(filepath)
    filename, _ = path.splitext(filename)
    #make filename just the name of the file,
    # with no leading directories and no extension

#    frequencies = [{key: l.count(True)/l.count(False) * 100 for key, l in counter.items()}] #had to be moved to loop
    frequenciesList = []
    plt.figure(figsize=(14,8)) #make a decent default size.
    for x in range(0, len(keywords)):
    #make a frequencies thing for each keyword, and plot each one onto the plot
        frequenciesList.append(
        {key: l.count(True)/len(l) * 100 for key, l in counters[x].items()})

        #find frequency of keyword use per date
        plt.plot(*zip(*sorted(frequenciesList[x].items())))

    plt.grid()
    #because i think it looks better with the grid

    if args.case_sensitive:
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
    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        keywords_string = '_'.join(keywords)

        if len(keywords_string) > 200:
        #file name likely to be so long as to cause issues
            figname = input(
                "This graph is going to have a very long file name. Please enter a custom name(no need to add an extension): ")
        else:
            figname = "{} in {}".format(
                keywords_string, filename)

        plt.savefig("{}/{}.png".format(savefolder, figname))
    else:
    #if a save folder was not specified, just open a window to display graph
        plt.show()

if __name__ == "__main__":
    main()
