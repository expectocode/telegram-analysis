#!/usr/bin/env python3
"""
A program to extract raw text from Telegram chat log which is in json form
"""
import argparse
from json import loads

def main():

    parser = argparse.ArgumentParser(
            description="analyse a json output of telegram backup utility")
    parser.add_argument('filepath', help='the json file to analyse')

    args=parser.parse_args()
    filepath = args.filepath

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            #check the event is the sort we're looking for
            if "from" in event and "text" in event:
                #do i need the "from" here?
                print(event["text"])

if __name__ == "__main__":
    main()
