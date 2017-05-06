#!/usr/bin/env python3
"""
A program to find the most common lines in an input.
Developed to find most common messages in a chatlog
"""

from sys import stdin
import argparse
import matplotlib.pyplot as plt
from collections import Counter

def main():
    """
    main function
    """

    parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description='Find the most commonly repeated lines and their frequencies from an input.',
            epilog="""Example usage:
Get all text from a chat and find the most repeated messages:
    ./getalltext.py chat_name.jsonl | ./mostcommonphrases.py
Find the most repeated lines in a textfile:
    ./mostcommonphrases.py < textfile.txt
Not recommended:
    running this program with no arguments. This will wait for input and EOF."""
    )
    parser.add_argument(
            '-g','--graph',
            help='Create a bar chart showing the most common phrases',
            action='store_true')
    parser.add_argument('-o', '--output-folder',
            help='the folder to save the bar chart image in.'
            'Using this option will make the graph not display on screen. '
            'This option has no effect if -g/--graph is not specified.')
    parser.add_argument('-n','--number-of-phrases',
            help='The number of phrases to print. Default 20.',
            type=int)
    parser.add_argument('-b','--number-of-bars',
            help='The number of bars to show on the bar chart (cannot be larger than number of phrases). Default 20.',
            type=int)
    parser.add_argument(
            '-s','--figure-size',
            help='the size of the figure shown or saved (X and Y size). '
            'Choose an appropriate value for your screen size. Default 14 8. '
            'This option has no effect if -g/--graph is not specified.',
            nargs=2,type=int
            )

    args = parser.parse_args()

    number_of_phrases = args.number_of_phrases if (args.number_of_phrases is not None) else 20
    if args.number_of_bars is not None:
        #its defined, lets make sure its sane
        if args.number_of_bars > number_of_phrases:
            number_of_bars = number_of_phrases
        else:
            number_of_bars = args.number_of_bars
    elif args.number_of_phrases is not None:
        #its not defined, but if the other is let's make them equal
        number_of_bars = number_of_phrases
    else:
        #its not defined and neither is the other.
        number_of_bars = number_of_phrases
    if args.figure_size is not None:
        figure_size = (args.figure_size[0],args.figure_size[1])
    else:
        figure_size = (14,8)

    sortedfreqs = Counter(map(lambda x: x.rstrip().lower(),stdin)
            ) .most_common(number_of_phrases)
    #most common phrases from a counter object which takes all the lines from stdin and strips em

    #delete all with freq 1
    sortedfreqs  = [x for x in sortedfreqs if x[1] != 1]

    print(sortedfreqs) # output the list

    if args.graph:

        #now just deal with the top 10% of phrases
        sortedfreqs = sortedfreqs[:number_of_bars]
        #frequency_threshold = sortedfreqs[len(sortedfreqs)//5][1]
        #sortedfreqs = [x for x in sortedfreqs if x[1] > frequency_threshold]
        phrases,frequencies = list(zip(*sortedfreqs))
        y_pos = range(len(phrases))
        width = 0.6
        plt.figure(figsize=figure_size)
        plt.bar([x*2 for x in y_pos],frequencies,align='center',width=width)
        plt.ylabel('frequency')
        plt.title('most common phrases')
        plt.xticks([x*2+width/3 for x in y_pos], phrases,rotation=25,ha='right')
        #list comp makes the coords all shifted slightly, rotation is for readability,
        #ha=right ensures thaht the rotated labels have their right side under the bar they refer to
        plt.show()
    else:
        #show a warning message if they use a graph arg and theres no --graph
        pass

if __name__ == "__main__":
    main()
