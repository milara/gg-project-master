import json
import re
import nltk
from collections import Counter

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_SET = set(OFFICIAL_AWARDS)

# Returns all tweet text from year in lowercase
def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            tweet_text_lst.append(tweet['text'].lower())

    return tweet_text_lst

def get_nominees(year):
    # Scanning forward words
    nominated_pattern = re.compile('nomin')
    win_words = ['got', 'won', 'wins', 'nomin']
    tweets_containing_won = list(filter(nominated_pattern.search, get_tweets(year)))

    award_tweets = []

    for tweet in tweets_containing_won:
        for win in win_words:
            if win in tweet:
                first, middle, rest = tweet.partition(win)
                print(first, "\n", middle, "\n", rest)
                #break
                
        #break
        #tokenized_match = nltk.tokenize.word_tokenize(middle.group(0))
        
        """ added_word = False
        for i, token in enumerate(tokenized_match):
            if token in ["for", "at", "on", "#"] or nltk.pos_tag([token])[0][1] in ["VB", "VBG", "VBD", "VBN", "VBP", "VBZ"]:
                award_tweets.append(' '.join(tokenized_match[:i]))
                added_word = True
                break
        
        if not added_word:
            award_tweets.append(match.group(0)) """
    
    award_names_dict = Counter()
    for tweet in award_tweets:
        splitted_word = tweet.split()
        for i in range(len(splitted_word)):
            temp = ' '.join(splitted_word[:i+1])
            award_names_dict[temp] = award_names_dict.get(temp, 0) + 1

    return {}

get_nominees('2013')