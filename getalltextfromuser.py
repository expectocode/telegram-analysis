#!/usr/bin/env python3
"""
A program to extract all text sent by a particular user from a Telegram chat log which is in json form
"""
import argparse
from json import loads

def main():

    parser = argparse.ArgumentParser(
        description="Extract raw text sent by a user from a json telegram chat log")
    parser.add_argument(
        'filepath', help='the json file to analyse')
    parser.add_argument(
        'username', help='the username of the person whose text you want')

    args=parser.parse_args()
    filepath = args.filepath
    username = args.username

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            if "from" and "text" in event:
                if "username" in event["from"]:
                    if event["from"]["username"] == username:
                        print(event["text"])

if __name__ == "__main__":
    main()
