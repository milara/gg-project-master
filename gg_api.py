'''Version 0.35'''
import nltk
import json


OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def loadTweet(filename):
    file = open(filename)
    raw_json = json.load(file)
    tweets = []
    for item in raw_json:
        tweets.append(item['text'])
    return tweets[:]

def clean_up_tweets(tweets):
    alphabet = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    cleaned = ''.join(filter(alphabet.__contains__, tweets))
    return cleaned 

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    hosts = []
    tweets = loadTweet(year)
    tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
    #cleaned_tweets = clean_up_tweets(tweets_lowered)
    
    #for some reason this method was leaving out some tweets that should have been included
    #hosts = [i for i in tweets if "hosting" in i or "hosts" in i or "host" in i]
    
    #so for now I'll just concatonate which seems to return everything it should
    hosts1 = [ i for i in tweets_lowered if "host" in i ]
    hosts2 = [ i for i in tweets_lowered if "hosts" in i ]
    hosts3 = [ i for i in tweets_lowered if "hosting" in i ]
    
    hosts = hosts1 + hosts2 + hosts3
    
    return hosts

def get_drama_awards(year):
    drama = []
    tweets = loadTweet(year)
    tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
    
    #for some reason this method was leaving out some tweets that should have been included
    #hosts = [i for i in tweets if "hosting" in i or "hosts" in i or "host" in i]
    
    #so for now I'll just concatonate which seems to return everything it should
    drama1 = [ i for i in tweets_lowered if "drama" in i]
    
    drama = drama1
    
    return drama

def get_comedy_or_musical_awards(year):
    comedy_or_musical = []
    tweets = loadTweet(year)
    tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
    
    #for some reason this method was leaving out some tweets that should have been included
    #hosts = [i for i in tweets if "hosting" in i or "hosts" in i or "host" in i]
    
    #so for now I'll just concatonate which seems to return everything it should
    comedy_or_musical1 = [ i for i in tweets_lowered if "comedy or musical" in i]
    
    comedy_or_musical = comedy_or_musical1
    
    return comedy_or_musical


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = []
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    nominees = {}
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    winners = {}
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    presenters = {}
    # Your code here
    return presenters

def extract_text(tweet):
    return tweet['text']#.lower()

def extract_entities(text):
    tokens = nltk.word_tokenize(text)
    chunks = nltk.chunk.ne_chunk(nltk.pos_tag(tokens))
    entities = []
    for c in chunks:
        if type(c) is not tuple:
            #print(c.leaves())
            entities.append(' '.join(leaf[0] for leaf in c.leaves()))
    return entities

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    with open('gg2013.json') as t:
        tweets = json.load(t)
    #print(extract_text(tweets[0]))
    for i in range(17000, 17008):
        #print(extract_text(tweets[i]))
        print(extract_entities(extract_text(tweets[i])))
    #
    return

#if __name__ == '__main__':
#    main()

get_comedy_or_musical_awards('gg2013.json')
