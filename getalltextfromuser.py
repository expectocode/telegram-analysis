#!/usr/bin/env python3
import argparse
from json import loads

parser = argparse.ArgumentParser(description="analyse a json output of telegram backup utility")
parser.add_argument('filename', help='the json file to analyse')
parser.add_argument('username', help='the username of the person whose text you want')

args=parser.parse_args()
filename = args.filename
username = args.username

#print(loads(test_json)[0]["text"])
#0 is the index of the load in the loads
#text is the json thing

file = open(filename,'r')
data = []

for line in file.readlines():
    data.append(loads(line))

#print(data[0]["text"])

data.reverse()

for message in data:
    try:
        if message["from"]["username"] == username:
            print(message["text"])

    except Exception:
        pass

#print(data)
file.close()
