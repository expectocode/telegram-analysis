#!/usr/bin/env python3
from json import loads
import argparse

parser = argparse.ArgumentParser(
        "Print all the pinned text messages from a Telegram chat log")
parser.add_argument(
        'file',
        help='path to the json file (chat log) to analyse')

args = parser.parse_args()

with open(args.file,'r') as f:
    jsn = [loads(line) for line in f.readlines()]

pins = [x['reply_id'] for x in jsn if
        'text' in x and x['text'] == 'pinned the message']
#reply_id is the ID of the message that has been pinned.
pin_msgs = [x for x in jsn if x['id'] in pins if 'text' in x]
#ignore pins with no text

_ = [print(x['text'],'\n------------------') for x in pin_msgs]
