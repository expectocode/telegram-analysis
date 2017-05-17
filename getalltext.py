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
    parser.add_argument('-u','--usernames', help='Show usernames before messages. '
                        'If someone doesn\'t have a username, the line will start with "@: ".'
                        'Useful when output will be read back as a chatlog.',
                        action='store_true')
    parser.add_argument('-n','--no-newlines', help='Remove all newlines from messages. Useful when '
                        'output will be piped into analysis expecting newline separated messages. ',
                        action='store_true')

    args=parser.parse_args()
    filepath = args.filepath

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            #check the event is the sort we're looking for
            if "from" in event and "text" in event:
                if args.usernames:
                    if 'username' in event['from']:
                        print('@' + event['from']['username'],end=': ')
                    else:
                        print('@',end=': ')
                if args.no_newlines:
                    print(event['text'].replace('\n',''))
                else:
                    print(event["text"])

if __name__ == "__main__":
    main()
