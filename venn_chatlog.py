#!/usr/bin/env python3
"""
A program to plot the overlap of chats
"""
import argparse
from json import loads
from os import path
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Visualise the overlap between 2 or 3 chats \n but note that the program is not truly accurate as it counts users who have left to be part of a chat. Also note that for 3 chats, perfect geometry may be impossible.")
    parser.add_argument(
            '-f','--files',
            help='paths to the json file(s) (chat logs) to analyse. Note these must be at the end of the arguments.',
            nargs='+')
    parser.add_argument('-o', '--output-folder',
            help='the folder to save the graph image in')

    args = parser.parse_args()
    filepaths = args.files
    savefolder = args.output_folder

    filenames = []
    users = [[] for filepath in filepaths]
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
                    users[index].append(event['action']['user']['id'])
                elif "action" in event and event['action']['type'] == 'chat_add_user_link':
                    #print(event['from']['id'], ":", event['from']['print_name'])
                    users[index].append(event['from']['id'])
        #print("index:",index)
        #print("len(users):",len(users))
        print(len(users[index]),"users")

    if len(users) == 2:
        venn2([set(users[0]), set(users[1])],(filenames[0], filenames[1]))
    elif len(users) == 3:
        venn3([set(users[0]), set(users[1]), set(users[2])],(filenames[0], filenames[1], filenames[2]))

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
