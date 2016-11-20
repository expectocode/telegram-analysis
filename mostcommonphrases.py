#!/usr/bin/env python3
#a program to find the most common lines (messages) in an input (tg log)
#TODO:optimise this whole program

from sys import stdin

#homemade way to find the index of the list containing a certain message inside a list of lists
#probably horrible inefficient
def where_in_list( phrase, listToSearch ):
    for thing in listToSearch:
        if phrase in thing:
            return listToSearch.index(thing)
        else:
            continue
    return -1
    #if it hasn't found a match in the for

def getKey(item):
    return item[1]

messagesFrequencyList = [["example phrase", 1]]

#print(type(messagesFrequencyList[0][0]))
#print(messages[0][0])

for line in stdin:
    message = line.rstrip().lower()
    indexFound = where_in_list(message, messagesFrequencyList)
    if indexFound > -1:
        messagesFrequencyList[indexFound][1]+=1 #increase frequency
    else:
        messagesFrequencyList.append([message,1])

#delete all with freq 1
#go through the list of lists backwards. -1 is magic ;)
for x in range(len(messagesFrequencyList) -1, -1, -1):
    if messagesFrequencyList[x][1] == 1: #if freq is 1
        del messagesFrequencyList[x]

print(sorted(messagesFrequencyList, key=getKey, reverse=True))
