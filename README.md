#telegramAnalysis
Made for dealing with the output of https://github.com/tvdstaaij/telegram-history-dump

Common usage:

`./getalltextfromuser.py json/chat_name.jsonl username_without_at_sign | ./mostcommonphrases.py | less` gives an output like:

![example of most common phrases output](/examples/phrases.jpg?raw=true)

`./phraseovertime.py chat_name.jsonl phrase` gives an output of a graph (made by using matplotlib) like:

![example of graph for phrase over time](/examples/graph.jpg?raw=true)
