'''Version 0.35'''
import nltk
import json
import random
from statistics import mode

# global variable for holding tweets, key: year, value: list of cleaned tweets
tweetdict = {}
OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def loadTweet(filename):
    file = open(filename)
    raw_json = json.load(file)
    tweets = []
    for item in raw_json:
        tweets.append(clean_up_tweets(item['text'].lower()))
    return tweets[:]

def test_sample(tweets, n):
    return random.sample(tweets,n)

def clean_up_tweets(tweets):
    alphabet = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    cleaned = ''.join(filter(alphabet.__contains__, tweets))
    return cleaned 

def remove_rts(tweets):
    for i in tweets[:]:
        if i.startswith('rt'):
            tweets.remove(i)
    return tweets

#gets tweets related to hosting
def get_relevant_host_tweets(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''

    host_tweets = []

    tweets = tweetdict[year]
    tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
    
    hosts1 = [ i for i in tweets_lowered if "host" in i ]
    hosts2 = [ i for i in tweets_lowered if "hosts" in i ]
    hosts3 = [ i for i in tweets_lowered if "hosting" in i ]
    
    host_tweets = hosts1 + hosts2 + hosts3
    
    return host_tweets

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    hosts = []
    # Find tweets related to hosting
    relevant_tweets = get_relevant_host_tweets(year)
    tweets = tweetdict[relevant_tweets]
    #list of potential hosts
    candidates = []
    # Iterate through tweets, detecting names for each one
    for tweet in tweets:
        if any(name in tweet for name in NAMES.lower()) in tweet.lower():
            tokens = nltk.word_tokenize(tweet.lower())
            idx = tokens.index(name)
            hosts.append(tokens[idx])
    return hosts

def get_relevant_award_tweets(year):
    drama = []
    tweets = tweetdict[year]
    tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
    
    drama1 = [ i for i in tweets_lowered if "best" in i]
    
    drama = drama1
    
    
    
    return drama


# def get_drama_awards(year):
#     drama = []
#     tweets = tweetdict[year]
#     tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
#     drama1 = [ i for i in tweets_lowered if "drama" in i]
    
#     drama = drama1
    
#     return drama

# def get_comedy_or_musical_awards(year):
#     comedy_or_musical = []
#     tweets = tweetdict[year]
#     tweets_lowered = [clean_up_tweets(x.lower()) for x in tweets]
    
#     comedy_or_musical1 = [ i for i in tweets_lowered if "comedy or musical" in i]
    
#     comedy_or_musical = comedy_or_musical1
    
#     return comedy_or_musical


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
    tweets = tweetdict[year]
    if year < 2018:
        awards = OFFICIAL_AWARDS_1315
    else:
        awards = OFFICIAL_AWARDS_1819
    # Iterate through awards, picking a winner for each one
    for award in awards:
        # initialize dictionary
        winners[award] = ''
        # List of potential winners
        candidates = []
        for tweet in tweets:
            # Find tweets that contain the award 
            # (may need to rephrase award names for some)
            if award in tweet.lower():
                tokens = nltk.word_tokenize(tweet.lower())
                # look for winning key words "wins" and "won" (more can be added)
                if "wins" in tokens:
                    idx = tokens.index("wins")
                    for i in range(idx):
                        candidate = ' '
                        candidate = candidate.join(tokens[i:idx])
                        candidates.append(candidate)
                if "won" in tokens:
                    idx = tokens.index("won")
                    for i in range(idx):
                        candidate = ' '
                        candidate = candidate.join(tokens[i:idx])
                        candidates.append(candidate)
        if not candidates:
            winners[award] = ''
        else:
            winners[award] = mode(candidates)

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
            entities.append(' '.join(leaf[0] for leaf in c.leaves()))
    return entities

def make_tweet_dict():
    # Makes a dictionary of all tweets with the year as the key
    tweetdict = {}

    tweetdict[2013] = loadTweet('gg2013.json')
    tweetdict[2015] = loadTweet('gg2015.json')

    # smaller sample for testing
    tweetdict[2013] = test_sample(tweetdict[2013],2000)
    tweetdict[2015] = test_sample(tweetdict[2015],2000)
    return tweetdict

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    global tweetdict 
    tweetdict = make_tweet_dict()
    # Filtering may need to be done here

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
    pre_ceremony()
    print(remove_rts(tweetdict[2013]))


    

#if __name__ == '__main__':
#    main()
main()

