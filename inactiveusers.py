#!/usr/bin/env python3
"""
A quick hack of a program to find a rough percentage of users in a chat who have sent less than 3 messages.

Warning: written at 1AM
"""
import argparse
from json import loads
from os import path
from collections import defaultdict

def main():
    """
    main function
    """
    #cutoff for a 'non active' user
    minimum = 3
    non_active_users = 0
    active_users = 0
    parser = argparse.ArgumentParser(description="Find the number of inactive users (users who have sent less than 3 messages) in a Telegram chat")
    parser.add_argument('filepath', help='the jsonl chatlog file to analyse')

    args = parser.parse_args()
    filepath = args.filepath

    _, filename = path.split(filepath)
    filename, _ = path.splitext(filename)
    #make filename just the name of the file, with no leading directories and no extension

    counter = defaultdict(int) #store events from each user
    #names = {} #dict
    total_datapoints = 0

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            if "from" in event:
                if "peer_id" in event["from"] and "print_name" in event["from"]:
                    total_datapoints += 1
                    user = event['from']['peer_id']
                    counter[user] += 1

    trimmedCounter = defaultdict(int)

    for person, frequency in counter.items():
        if frequency < minimum:
            #trimmedCounter["other"] += frequency
            non_active_users += 1
        else:
            #trimmedCounter[names[str(person)]] = frequency
            active_users += 1

    print('For this chat, there were {} users who sent less than'
            ' {} messages, out of a total of {}.'.format(
                non_active_users,minimum,non_active_users+active_users))
    print("That's", round(100* non_active_users/(non_active_users + active_users),1), "%!")

#    print(type(*sorted(counter.items())))
 #   plt.pie(*zip(*sorted(counter.items())))

if __name__ == "__main__":
    main()
