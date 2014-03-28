from os import listdir

import pickle
import re

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

    
if __name__ == "__main__":
    corpus = read_data()
    print(corpus)
    
