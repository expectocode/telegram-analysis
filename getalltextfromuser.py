#!/usr/bin/env python3
"""
A program to extract all text sent by a particular user from a Telegram chat log
"""
import argparse
from json import loads

def main():

    parser = argparse.ArgumentParser(
        description="Extract all raw text sent by a specific user in a specific Telegram chat")
    parser.add_argument(
        'filepath', help='the jsonl chatlog file to analyse')
    parser.add_argument(
        'username', help='a username of the person whose text you want (without @ sign), case insensitive')

    args=parser.parse_args()
    filepath = args.filepath
    username = args.username.lower()

    user_id = ""

    #first, get the ID of the user with that username.
    #ideally, this only runs for less than 100 messages, if its a recent username
    #TODO: allow user id as argument
    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
        #check the event is the sort we're looking for
            if "from" in event:
                if "username" in event["from"]:
                    if event["from"]["username"].lower() == username:
                        user_id = event['from']['id']
                        break
    if user_id == "":
        print("username not found in chatlog")
        exit()

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
        #check the event is the sort we're looking for
            if "from" in event and "text" in event:
                if user_id == event["from"]["id"]:
                    print(event["text"])

if __name__ == "__main__":
    main()
