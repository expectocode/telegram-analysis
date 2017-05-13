#!/usr/bin/env python3
"""
A program to extract raw text from Telegram chat log
"""
import argparse
from json import loads

def main():

    parser = argparse.ArgumentParser(
            description="Extract all raw text from a specific Telegram chat")
    parser.add_argument('filepath', help='the json chatlog file to analyse')
    parser.add_argument('-u','--usernames', help='Show usernames before messages',action='store_true')

    args=parser.parse_args()
    filepath = args.filepath

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            #check the event is the sort we're looking for
            if "from" in event and "text" in event:
                if args.usernames:
                    print(event['from']['username'],end=': ')
                #do i need the "from" here?
                print(event["text"])

if __name__ == "__main__":
    main()
