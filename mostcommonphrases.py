#!/usr/bin/env python3
#a program to find the most common lines (messages) in an input (tg log)

from sys import stdin
import matplotlib.pyplot as plt
from collections import Counter

def main():

    number_of_phrases = 20
    sortedfreqs = Counter(map(lambda x: x.rstrip().lower(),stdin)).most_common(3*number_of_phrases)

    #delete all with freq 1
    sortedfreqs  = [x for x in sortedfreqs if x[1] != 1]

    print(sortedfreqs) # output the list
    #now just deal with the top 10% of phrases
    sortedfreqs = sortedfreqs[:number_of_phrases]
    #frequency_threshold = sortedfreqs[len(sortedfreqs)//5][1]
    #sortedfreqs = [x for x in sortedfreqs if x[1] > frequency_threshold]
    phrases,frequencies = list(zip(*sortedfreqs))
    y_pos = range(len(phrases))
    width = 0.6
    plt.figure(figsize=(13,9))
    plt.bar([x*2 for x in y_pos],frequencies,align='center',width=width)
    plt.ylabel('frequency')
    plt.title('most common phrases')
    plt.xticks([x*2+width/3 for x in y_pos], phrases,rotation=25,ha='right')
    #list comp makes the coords all shifted slightly, rotation is for readability,
    #ha=right ensures thaht the rotated labels have their right side under the bar they refer to
    plt.show()

if __name__ == "__main__":
    main()
