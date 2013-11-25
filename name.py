from os import listdir
import re


dir = "names"
fname_pattern = re.compile("yob[0-9]{4}.txt")
alpha = 'abcdefghijklmnopqrstuvwxyz'

names  = {'f':set(),'m':set()}
ngrams = {'f':{letter: 0 for letter in alpha}, 'm':{letter: 0 for letter in alpha}}
total_letters = 0

def read_files():
    files = fname_pattern.findall(' '.join(listdir(dir)))
    for f in files:
        for line in open(dir + '/' + f, 'r').readlines():
            s = line.split(',')
            names.get(s[1].lower()).add(s[0].lower()) # s[1] is the sex s[0] is the name

def populate_corpus():
    tl = 0
    if len(names.get('f')) == 0:
        read_files()
    for sex in names:
        for name in names.get(sex):
            tl += len(name)
            for letter in name:
                ngrams[sex][letter] += 1
                
if __name__ == "__main__":
    read_files()
    populate_corpus()
    total_letters = 0
    for l in ngrams['f']:
        total_letters += ngrams.get('f').get(l)
    for letters in ngrams.get('f'):
        print(letters + " : " + str(ngrams['f'][letters])+ " : " + str(ngrams['f'][letters] / total_letters))

