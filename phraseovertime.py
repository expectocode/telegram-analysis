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
    parser.add_argument('-i', '--insensitive', help='make the phrase search case insensitive', action='store_true')
    parser.add_argument('-o', '--output-folder', help='output the figure to image file in this folder')
    parser.add_argument('keyword', help='the keyword to search for (note that it must be at the end for multiple words)')

    args = parser.parse_args()
    filepath = args.filepath
    keyword = args.keyword
    savefolder = args.output_folder

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)

        counter = defaultdict(list)
        for event in events:
            if "text" in event:
                if args.insensitive:
                    if "text" in event:
                        day = date.fromtimestamp(event["date"])
                        counter[day].append("text" in event and keyword in event["text"].lower())
                else:
                    day = date.fromtimestamp(event["date"])
                    counter[day].append("text" in event and keyword in event["text"])

    _, filename = path.split(filepath)
    filename, _ = path.splitext(filename)

    frequencies = {key: l.count(True)/l.count(False) * 100 for key, l in counter.items()}
    plt.figure(figsize=(17,10))
    plt.plot(*zip(*sorted(frequencies.items())))
    if args.insensitive:
        postfix=", case-insensitive"
    else:
        postfix=""
    plt.title("usage of \"{}\" in {}{}".format(keyword, filename, postfix)) #file name minus extension jsonl"

    plt.ylabel("Percentage of messages containing \"{}\"".format(keyword), size=14)
    if savefolder is not None:
        plt.savefig("{}/{}_in_{}.png".format(savefolder, keyword, filename))
    else:
        plt.show()

if __name__ == "__main__":
    main()
