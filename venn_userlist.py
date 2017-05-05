#!/usr/bin/env python3
"""
A program to plot the overlap of chats
"""
import argparse
from json import loads
import matplotlib.pyplot as plt
from matplotlib_venn import venn2, venn3

def main():
    """
    main function
    """
    parser = argparse.ArgumentParser(
            description="Visualise the overlap between 2 or 3 chats. Note that for 3 chats, perfect geometry may be impossible.")
    parser.add_argument(
            '-f','--file',
            help='paths to the json userlist',
            required = True)
    parser.add_argument(
            '-c','--chat_names',
            help="Names (or part of names) of the chats you're interested in, case insensitive",
            nargs='+',
            required = True)
    parser.add_argument('-o', '--output-folder',
            help='the folder to save the graph image in')

    args = parser.parse_args()
    filepath = args.file
    names = args.chat_names
    savefolder = args.output_folder

    full_names = []
    userlists = [[] for name in names]

    j = loads(open(filepath,'r').read())
    list_of_chats = [j[x] for x in j]
    titles = [x['title'] for x in list_of_chats]

    #this code works but doesn't sort j by chat title length, which is important due to the user title search thing
    #for index,name in enumerate(names):
    #    found_chat = False
    #    for chat_id in j:
    #        if name in j[chat_id]['title'] and len(list(j[chat_id]['users'])) > 0:
    #            #because some of the memberlist things come to zero
    #            #print(j[chat_id]['users'])
    #            full_names.append(j[chat_id]['title'])
    #            userlists[index].extend( [user['id'] for user in j[chat_id]['users']] )
    #            found_chat = True
    #
    #    if not found_chat:
    #        print("Could not find result for", name)
    #        exit()

    #magic
# [x[1]['title'] for x in sorted(list(j.items()), key=lambda a: len(a[1]['title']))]

    sorted_j = [ x for x in sorted(list(j.items()), key=lambda a: len(a[1]['title'])) if(len(x[1]['users']) > 0) ]
    #this makes the JSON input into a list of tuples (chat_id, info_dict) and also removes empty chats
    #the importance of sorting is so that search strings are first tested on the smaller titles
    #eg searching 'GNU/Linux' should yield 'GNU/Linux' before 'GNU/Linux Chat' (real example)
    for index,name in enumerate(names):
        found_chat = False
        for chat in sorted_j:
            #lowercase because case sensitivity annoyed me
            if name.lower() in chat[1]['title'].lower() and len(chat[1]['users']) > 0 and (not found_chat):
                #because some of the memberlist things come to zero
                #print(j[chat_id]['users'])
                full_names.append(chat[1]['title'])
                userlists[index].extend( [user['id'] for user in chat[1]['users']] )
                found_chat = True

        if not found_chat:
            print("Could not find result for", name)
            exit()

    if len(userlists) == 2:
        venn2([set(userlists[0]), set(userlists[1])],(full_names[0], full_names[1]))
    elif len(userlists) == 3:
        venn3([set(userlists[0]), set(userlists[1]), set(userlists[2])],(full_names[0], full_names[1], full_names[2]))

    #print(users)

    if savefolder is not None:
    #if there is a given folder to save the figure in, save it there
        names_string = '_'.join(full_names)

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
