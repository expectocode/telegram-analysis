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
            description="Visualise the usage of a phrase in a chat over time")
    parser.add_argument('filepath', help='path to the json file (chat log) to analyse')
    parser.add_argument('-c', '--case-sensitive', help='make the phrase search case sensitive', action='store_true')
    parser.add_argument('-o', '--output-folder', help='output the figure to image file in this folder')
    parser.add_argument('keywords', help='the keyword(s) to search for (note that these must be at the end of the argument list)', nargs=argparse.REMAINDER)

    args = parser.parse_args()
    filepath = args.filepath
    keywords = args.keywords
    savefolder = args.output_folder

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        counters = [defaultdict(list) for keyword in keywords]
        for event in events:
            for keyword in keywords:
                if "text" in event:
                    if args.case_sensitive:
                        if "text" in event:
                            day = date.fromtimestamp(event["date"])
                            counters[keywords.index(keyword)][day].append("text" in event and keyword in event["text"])
                    else:
                        day = date.fromtimestamp(event["date"])
                        counters[keywords.index(keyword)][day].append("text" in event and keyword in event["text"].lower())

    _, filename = path.split(filepath)
    filename, _ = path.splitext(filename)

#    frequencies = [{key: l.count(True)/l.count(False) * 100 for key, l in counter.items()}]
    frequenciesList = []
    plt.figure(figsize=(17,10))
    for x in range(0, len(keywords)):
        frequenciesList.append({key: l.count(True)/l.count(False) * 100 for key, l in counters[x].items()})
        plt.plot(*zip(*sorted(frequenciesList[x].items())))

    plt.legend(keywords)
    if args.case_sensitive:
        postfix=", case sensitive"
    else:
        postfix=", case insensitive"
    plt.title("usage of {} in {}{}".format(keywords, filename, postfix)) #file name minus extension jsonl"

#    plt.ylabel("Percentage of messages containing \"{}\"".format(keyword), size=14)
    plt.ylabel("Percentage of messages containing keywords".format(keyword), size=14)
    if savefolder is not None:
        plt.savefig("{}/{}_in_{}.png".format(savefolder, keyword, filename))
    else:
        plt.show()

if __name__ == "__main__":
    main()
