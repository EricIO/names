from functools import reduce
from os import listdir

import math
import pickle
import re
import operator
import sys

def read_data():
    try:
        return pickle.load(open('data.dat', 'rb'))
    except IOError:
        print('Unable to load file, reading data from text files')
        
    files = fname_pattern.findall(' '.join(listdir('names')))
    names  = {'f':set(),'m':set()}
    fname_pattern = re.compile("yob[0-9]{4}.txt")
    for f in files:
        for line in open('names' + '/' + f, 'r').readlines():
            s = line.split(',')
            names.get(s[1].lower()).add(s[0].lower()) # s[1] is the sex s[0] is the name

    corpus = populate_corpus(names)
    pickle.dump(corpus, open('data.dat', 'wb'))
    return corpus
            
def populate_corpus(names):
    grams = {'f':{},'m':{}}
    for sex in names:
        for name in names.get(sex):
            gram = bigram('<' + name + '>')
            for l in gram:
                if grams[sex].get(l) == None:
                    grams[sex][l] = 1
                else:
                    grams[sex][l] += 1
    return grams

def bigram(name):
    '''Returns all the bigrams for a string'''
    return [name[i:i+2] for i in range(1+len(name)-2)]

def probability(name, data):
    '''Computes the probabilty for the gender of the name''' 
    female_total, male_total  = total(data)
    grams = bigram('<' + name.lower() + '>')
    female_probs = [(i + 1) / (female_total + len(data['f'])) for i in counts(data, grams, 'f')]
    male_probs = [((i + 1)/ (male_total + len(data['m']))) for i in counts(data, grams, 'm')]
    
    return reduce(operator.add, [math.log(i) for i in female_probs]), reduce(operator.add, [math.log(i) for i in male_probs])

def counts(data, grams, gender):
    return [data[gender].get(i, 0) for i in grams]

def total(data):
    ftot, mtot = 0, 0
    for _, v in data['f'].items():
        ftot += v
    for _, v in data['m'].items():
        mtot += v
    return ftot, mtot

def gender(name,data):
    pf,pm = probability(name,data)
    if pf > pm:
        return 'F'
    else:
        return 'M'
        
    
    
if __name__ == "__main__":
    corpus = read_data()
    if len(sys.argv) > 1:
        g = gender('<' + sys.argv[1] + '>', corpus)
        if g == 'F':
            print('My guess is that you are a female!')
        else:
            print('My guess is that you are a male!')
    else:
        tot, hits, misses, unknown = 0,0,0,0
        f = open('test-data', 'r')
        for line in f.readlines():
            data = line.strip('\n').split(',')
            g = gender(data[0], corpus)
            print("You guessed {0} was {1} and was {2}".format(data[0],g, data[1]))
            tot += 1
            if g == data[1]:
                hits += 1
            else:
                misses += 1
            print('Total: {0}\nHits: {1}\nMisses: {2}\nUnknow: {3}\nCorrectness: {4}'
                  .format(tot, hits, misses, unknown, (hits/tot * 100)))
            
            
