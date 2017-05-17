#!/usr/bin/env python3
"""
A program to plot the users joining a chat over time. Note that leaving events are not noted.
TODO: support multiple chats.
TODO: support saving to image
"""
import argparse
import os
from json import loads
from datetime import date
from collections import defaultdict
from pprint import pprint

import matplotlib.pyplot as plt

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Visualise the growth a chat over time - note that leavers are not recorded, so this program can only show the join rate.")
    parser.add_argument('path', help='the json file (chat log) to analyse')

    args = parser.parse_args()
    path = args.path

    with open(path, 'r') as f:
        events = (loads(line) for line in f)

        counter = defaultdict(int)
        for event in events:
            if "action" in event and (event["action"]["type"] == "chat_add_user" or event['action']['type'] == 'chat_add_user_link'):
                day = date.fromtimestamp(event["date"])
                counter[day] += 1

    filename = path.splitext(path.split(filepath)[-1])[0]

    #frequencies = {key: l.count(True)/l.count(False) * 100 for key, l in counter.items()}
    users_per_day = sorted(counter.items())

    u_count = 0
    for idx, (day, users) in enumerate(users_per_day):
        u_count += users
        users_per_day[idx] = (day, u_count)

    print(users_per_day)
    plt.plot(*zip(*users_per_day))
    plt.title('members in "{}"'.format(filename))

    plt.show()

if __name__ == "__main__":
    main()
