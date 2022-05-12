import json
import re
import nltk
from collections import Counter

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

def find_word(text, search):

   result = re.findall('\\b'+search+'\\b', text, flags=re.IGNORECASE)
   if len(result)>0:
      return True
   else:
      return False

def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            tweet_text_lst.append(tweet['text'])

    return tweet_text_lst

def get_presenters(year):
    presenters_tweets = []
    presenter_pattern = re.compile('present')
    tweets_containing_present = list(filter(presenter_pattern.search, get_tweets(year)))
    for tweet in tweets_containing_present:
        #if re.search("([A-Za-z]+[\s-]?[A-Za-z]+(and)?)+\spresent", tweet):
        #if re.search(" [A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,1}\s+[A-Z]([a-z]+|\.)", tweet):
        pattern1 = re.search("([A-Z][a-z]*)[\s-]([A-Z][a-z]*)[\s-](and)[\s-]([A-Z][a-z]*)[\s-]([A-Z][a-z]*)", tweet)
        pattern2 = re.search("[A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[A-Z][a-z\-]+){0,1}\s+[A-Z]([a-z]+|\.)", tweet)
        if pattern1:
            name1 = pattern1.group(1) + ' ' + pattern1.group(2)
            name2 = pattern1.group(4) + ' ' + pattern1.group(5)
            presenters_tweets.append(name1)
            presenters_tweets.append(name2)
        elif pattern2:
            name1 = pattern2.group(0)
            name2 = pattern2.group(2)
            presenters_tweets.append(name1)
    presenters = Counter()
    presenters.update(presenters_tweets)
    print(presenters)
    return
  

   



get_presenters(2013)