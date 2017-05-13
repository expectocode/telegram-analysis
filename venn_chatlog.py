#!/usr/bin/env python3
"""
A program to plot the overlap of chats
"""
import argparse
from json import loads
from os import path
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3
from collections import defaultdict

def get_active_users(filepath):
    minimum = 20
    counter = defaultdict(int) #store events from each user
    #names = {} #dict
    active_users = set()

    with open(filepath, 'r') as jsonfile:
        events = (loads(line) for line in jsonfile)
        for event in events:
            if "from" in event:
                if "id" in event["from"] and "print_name" in event["from"]:
                    user = event['from']['id']
                    counter[user] += 1

    for person, frequency in counter.items():
        if frequency > minimum:
            active_users.add(person)

    return active_users

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Visualise the overlap between 2 or 3 chats \n but note that the program is not truly accurate as it counts users who have left to be part of a chat. Also note that for 3 chats, perfect geometry may be impossible.")
    parser.add_argument(
            '-f','--files',
            help='paths to the json file(s) (chat logs) to analyse. Note these must be at the end of the arguments.',
            nargs='+',
            required = True)
    parser.add_argument('-a','--active-users',
            help='Only look at active users (users who have sent more than 3 messages)',
            action='store_true')
    parser.add_argument('-o', '--output-folder',
            help='the folder to save the graph image in')

    args = parser.parse_args()
    filepaths = args.files
    savefolder = args.output_folder

    filenames = []
    users = [set() for filepath in filepaths]
    #create a list of users for each chat

    for index,filepath in enumerate(filepaths):
        _, temp = path.split(filepath)
        filenames.append(temp)
        filenames[filepaths.index(filepath)] , _ = path.splitext(
                filenames[filepaths.index(filepath)] )

        print(filenames[index], "users:")

        with open(filepath, 'r') as jsonfile:
            events = (loads(line) for line in jsonfile)
            #generator, so whole file is not put in mem
            #a dict with dates as keys and frequency as values
            for event in events:
                if "action" in event and event["action"]["type"] == "chat_add_user":
                    #print(event['action']['user']['id'], ":", event['action']['user']['print_name'])
                    users[index].add(event['from']['id'])
                elif "action" in event and event['action']['type'] == 'chat_add_user_link':
                    #print(event['from']['id'], ":", event['from']['print_name'])
                    users[index].add(event['from']['id'])
        #print("index:",index)
        #print("len(users):",len(users))
        if args.active_users:
            active = get_active_users(filepath)
            users[index] = users[index] & active

        print(len(users[index]),"users")

    if len(users) == 2:
        venn2([users[0], users[1]],(filenames[0], filenames[1]))
    elif len(users) == 3:
        venn3([users[0], users[1], users[2]],(filenames[0], filenames[1], filenames[2]))

    #print(users)

    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        names_string = '_'.join(filenames)

        if len(names_string) > 200:
        #file name likely to be so long as to cause issues
            figname = input(
                "This diagram is going to have a very long file name. Please enter a custom name(no need to add an extension): ")
        else:
            figname = 'User overlap in {}'.format(names_string).replace('/','_')

        plt.savefig("{}/{}.png".format(savefolder, figname))
    else:
        plt.show()

if __name__ == "__main__":
    main()
