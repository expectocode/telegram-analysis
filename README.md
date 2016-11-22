#telegramAnalysis
Made for dealing with the output of https://github.com/tvdstaaij/telegram-history-dump

Common usage:

`./getalltextfromuser.py path/to/chat_name.jsonl username_without_at_sign | ./mostcommonphrases.py | less` gives an output of a list of commonly repeated messages by a certain user in a certain chat, like:

![example of most common phrases by user in chat output](/examples/userinchatphrases.jpg?raw=true)

`./getalltextfromuser.py path/to/chat_name.jsonl | ./mostcommonphrases.py` gives an output of a list of commonly repeated messages in a certain chat, like:

![example of most common phrases in chat output](/examples/chatphrases.jpg?raw=true)

`./phraseovertime.py path/to/chat_name.jsonl phrase` gives an output of a graph (made by using matplotlib)showing the usage of any number of given phrases or keywords in a single chat, like:

![example of graph for phrases over time](/examples/keywordsgraph.jpg?raw=true)

`./activityovertime.py path/to/chat_name.jsonl` gives an output of a graph (made by using matplotlib) showing the activity of a chat over time, like:

![example of graph for activity over time](/examples/activitygraph.jpg?raw=true)
