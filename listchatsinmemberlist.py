#!/usr/bin/env python3
"""
A program to tell you which chats you have in your memberlist, sorted by title length.
"""
import argparse
from json import loads

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Tell you which chats you have info on in your memberlist")
    parser.add_argument(
            'filepath',
            help='paths to the json userlist')

    args = parser.parse_args()
    filepath = args.filepath

    j = loads(open(filepath,'r').read())

    sorted_j = [ x for x in sorted(list(j.items()), key=lambda a: len(a[1]['title'])) if (len(x[1]['users']) > 0) ]
    #this makes the JSON input into a list of tuples (chat_id, info_dict) and also removes empty chats
    #the importance of sorting is so that search strings are first tested on the smaller titles
    #eg searching 'GNU/Linux' should yield 'GNU/Linux' before 'GNU/Linux Chat' (real example)
    for chat in sorted_j:
        #because some of the memberlist things come to zero
        print(chat[1]['title'])

if __name__ == "__main__":
    main()
