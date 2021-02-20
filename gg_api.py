'''Version 0.35'''
import nltk
import json
import random
from statistics import mode
from collections import Counter
import itertools
import operator


# global variable for holding tweets, key: year, value: list of cleaned tweets
global tweetdict#
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

NAMES = nltk.corpus.names.words('male.txt') + nltk.corpus.names.words('female.txt')
LOWERED_NAMES = [x.lower() for x in NAMES]

stop_words = nltk.corpus.stopwords.words('english')
stop_words.extend(['golden', 'globe', 'globes', 'goldenglobe', 'goldenglobes'])
stop_words = set(stop_words)

def loadTweet(filename):
    file = open(filename)
    raw_json = json.load(file)
    tweets = []
    for item in raw_json:
        tweets.append(item['text'].lower())
    return tweets

#takes all punctuation out of tweets
def clean_up_tweets(tweets):
    alphabet = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    cleaned = ''.join(filter(alphabet.__contains__, tweets))
    return cleaned 

def get_awards(year):
    print('getting awards')
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = OFFICIAL_AWARDS_1315
    return awards

def get_nominees(year):
    print('getting nominees')
    gen_relevant_tweets()
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    nominees = {}
    if year < '2018':
        awards = OFFICIAL_AWARDS_1315
    else:
        awards = OFFICIAL_AWARDS_1819
    
    for award in awards:
        #find relevant tweets to each award
        tweets = award_tweets[award]
        #initialize dict
        nominees[award]=[]
        #initialize potential candidates list
        candidates=[]
        for tweet in tweets: 
            if any('nomination' or 'nominees' or 'nominee' or 'nominated' or 'congrats' or 'congratulations' in tweet):
                extracted = extract_entities(tweet)
                for e in extracted:
                    if ' ' in e:
                        candidates.append(e)
            
        if candidates:
            listofnames=Counter(candidates).most_common(5)
            i=0
            while(i<5 and i<len(listofnames)):
                nominees[award].append(listofnames[i][0])
                i+=1
                
    return nominees

def get_relevant_award_tweets(award):
    relevant_tweets=[]
    for t in tweetdict:
        if get_similarity(award, t) > 0.8:
        #if award in t:
            if (('actor' in t) == ('actor' in award)) and (('actress' in t) == ('actress' in award)):
                relevant_tweets.append(t)
    return relevant_tweets

def get_award_tokens(award):
    award_tokens = nltk.word_tokenize(award)
    irrelevant_words = ['performance', 'by', 'an', 'in', 'a', '-', 'or', ',', 'made', 'for']
    award_tokens = [token for token in award_tokens if token not in irrelevant_words]
    return award_tokens

#ignore_words = ['by', 'performance', 'in', 'a', 'an', 'or', 'any', 'best', '-']
def get_similarity(award, tweet):
    tweet_tokens = nltk.word_tokenize(tweet)
    award_tokens = get_award_tokens(award)
    count=0
    for t in award_tokens:
        if t in tweet_tokens:
            count+=1
    return count/len(award_tokens)

def classify_award(award):
    if 'performance' in award or 'director' in award:
        kind = 'person'
    else:
        kind = 'title'
    return kind

more_irrelevant_words = ['http', 'rt', 'goldenglobes', 'goldenglobe']
def get_candidates(award):
    #print(award)
    winner_type = classify_award(award)
    candidates = []
    tweets = award_tweets[award]
    if winner_type == 'person':
        #print('finding person')
        for t in tweets:
            tokens = nltk.word_tokenize(t)
            names = [token for token in tokens if token in LOWERED_NAMES]
            for n in names:
                i = tokens.index(n)
                if i+1 < len(tokens):
                    candidates.append(tokens[i] + ' ' + tokens[i+1]) 
    if winner_type == 'title':
        for t in tweets:
            tokens = nltk.word_tokenize(t)
            if tokens[0] == 'rt':
                tokens = tokens[4:]
            if 'wins' in tokens:
                i = tokens.index('wins')
                #print('backward')
                tokens = tokens[:i]
                if not tokens[-1].isalpha():
                    tokens = tokens[:-1]
                #print(tokens)
                c = ''
                for token in tokens[::-1]:
                    if token.isalpha():
                        c = token + ' ' +c
                    else:
                        break
                candidates.append(c)
            elif 'to' in tokens:
                i = tokens.index('to')
                #print('forward')
                tokens = tokens[i+1:]
                if not tokens[0].isalpha():
                    tokens = tokens[1:]
                c = ''
                for token in tokens:
                    if token.isalpha():
                        c += ' ' + token
                    else:
                        break
                candidates.append(c)
    return candidates

def gen_relevant_tweets():
    global award_tweets
    award_tweets = {}
    # MAKE THIS MODULAR LATER
    for award in OFFICIAL_AWARDS_1315:
        award_tweets[award] = get_relevant_award_tweets(award)

def get_winner(year):
    print('getting winners')
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    winners = {}
    if year < '2018':
        #edit these lists to make them more casual
        awards = OFFICIAL_AWARDS_1315
    else:
        awards = OFFICIAL_AWARDS_1819
    
    for award in awards:
        print(award)
        winners[award] = ''
        #find relevant tweets to each award
        candidates = get_candidates(award)
        if candidates:
            winners[award] = Counter(candidates).most_common(1)[0][0]   
    return winners


def get_hosts(year):
    print('getting hosts')
    global tweetdict
    tweetdict = make_tweet_dict(year)
    print(len(tweetdict))
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    hosts = []
    # Find tweets related to hosting
    tweets = host_tweets = [ i for i in tweetdict if "host" in i ]
    #list of potential hosts
    candidates = []
    # Iterate through tweets, detecting names for each one
    """for t in tweets:
        people = [n in t for n in names]
        #candidates.(people) """
    for t in tweets:
        tokens = nltk.word_tokenize(t)
        names = [token for token in tokens if token in LOWERED_NAMES]
        for n in names:
            i = tokens.index(n)
            if i+1 < len(tokens):
                candidates.append(tokens[i] + ' ' + tokens[i+1])
    count = Counter(candidates).most_common(2)
    #print(count)
    hosts.append(count[0][0])
    hosts.append(count[1][0])
    return hosts

def get_presenters(year):
    print('getting presenter')
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    presenters = {}
    for award in OFFICIAL_AWARDS_1315:
        presenters[award] = 'your mom'
    # Your code here
    return presenters

def extract_entities(text):
    tokens = nltk.word_tokenize(text)
    chunks = nltk.chunk.ne_chunk(nltk.pos_tag(tokens))
    entities = []
    for c in chunks:
        if type(c) is not tuple:
            entity=' '.join(leaf[0] for leaf in c.leaves())
            if 'Golden' not in entity and 'Globes' not in entity:
                entities.append(entity)
            #entities.append(' '.join(leaf[0] for leaf in c.leaves()))
    return entities

def make_tweet_dict(year):
    # Makes a dictionary of all tweets with the year as the key
    print("making")
    tweets = loadTweet('gg' + str(year) + '.json')
    """ if year == 2013:
        tweetdict = loadTweet('gg2013.json')
    if year == 2015:
        tweetdict = loadTweet('gg2015.json') """
    # smaller sample for testing
    tweets = random.sample(tweets, 10000)
    return tweets

import csv
def read_names(year):
    global names
    names = []

    tsv_file = open("names.tsv", encoding='utf8')
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        if row[3] >= str(year) or row[3] == '\\N':
            #(row[3 ])
            names.append(row[1].lower())
    tsv_file.close()

def read_titles(year):
    global titles
    titles = []
    tsv_file = open("titles.tsv", encoding='utf8')
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    for row in read_tsv:
        if row[5] == str(year):
            titles.append([row[2].lower(), row[-1].lower()])
    tsv_file.close()

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    
    # Filtering may need to be done here
    #read_names(2013)
    #read_titles(2013)
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    # Make a dictionary of all tweets
    #global tweetdict
    
    #print(get_hosts(2013))
    
    #get_awards(year)
    #get_nominees(year)
    #get_presenters(year)
    
    #print(get_winner(2013))

    #print(get_relevant_award_tweets(OFFICIAL_AWARDS_1315[2]))
    #get_candidates(OFFICIAL_AWARDS_1315[2])


if __name__ == '__main__':
    pre_ceremony()
    main()