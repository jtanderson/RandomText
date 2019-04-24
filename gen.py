import numpy as np
import random
import _pickle as pickle
import sys
import getopt

def train():
    f = open("shakespeare.txt", 'r')

    lines = list(f)
    txt = ' '.join(lines)
    txt.replace('\n', '')

    txt = txt.split(" ")

    graph = {
            "^": {},
            "$": {}
            }

    prevWord = "^"

    txt = [w.strip() for w in txt]
    #txt = [w for w in txt if w.isalpha() and not w.isupper()]

    for word in txt:
        period = False

        while len(word) > 0 and word[-1] in [",", ";", ":", '"', '-', ']']:
            word = word[:-1]

        while len(word) > 0 and word[0] in [",", ";", ":", '"', "'", '[']:
            word = word[1:]

        if len(word) > 0 and word[-1] in [".", '?', '!']:
            word = word[:-1]
            period = True

        if len(word) is 0 or word.isupper() or not word.isalpha():
            continue

        if prevWord not in graph:
            graph[prevWord] = {}

        if word not in graph:
            graph[word] = {}

        if word in graph[prevWord]:
            graph[prevWord][word] += 1
        else:
            graph[prevWord][word] = 1

        if period:
            if "$" in graph[word]:
                graph[word]["$"] += 1
            else:
                graph[word]["$"] = 1
            prevWord = '^'
        else:
            prevWord = word
    return graph

def sample(graph):
    rtn = ["^"]
    while rtn[-1] is not "$":
        total = 0
        cur = rtn[-1]
        #print("Word: " + cur)
        #print(graph[cur])
        for w in graph[cur]:
            #print(w + " " + str(graph[cur][w]))
            total += graph[cur][w]
        r = random.randint(1,total)
        #print("r: %d, cur: %s, total: %d" % (r, cur, total))
        sub = 0
        for w in graph[cur]:
            sub += graph[cur][w]
            if r <= sub:
                rtn.append(w)
                break
    return " ".join(rtn)

def main(argv):
    inputfile = ''
    outputfile = ''
    weightFile = 'weights.dat'
    retrain = False
    msg = 'test.py -h -t'
    try:
        opts, args = getopt.getopt(argv,"ht", ["help", "train"])
                #"intext=","inweights=","outweights=","train"])
    except getopt.GetoptError:
        print(msg)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(msg)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--train"):
            retrain = True
    #print 'Input file is "', inputfile
    #print 'Output file is "', outputfile

    if retrain:
        weights = train()
        with open(weightFile, 'wb') as file:
            pickle.dump(weights, file)

    graph = {}
    with open(weightFile, 'rb') as file:
        graph = pickle.load(file)

    print(sample(graph))

if __name__ == "__main__":
    main(sys.argv[1:])








