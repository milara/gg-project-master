import json
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from difflib import SequenceMatcher
import Levenshtein

award_stop_words = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ',','is','best'])
nltk_stop_words = set(stopwords.words('english'))
nltk_stop_words.update(['http', 'golden', 'globes', 'goldenglobes', 'goldenglobe'])

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']


def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            tweet_text_lst.append(tweet['text'])

    return tweet_text_lst

def get_presenters(year):
    print("running")
    presenter_pattern = re.compile('present')
    tweets_containing_present = list(filter(presenter_pattern.search, get_tweets(year)))
    awards = dict.fromkeys(OFFICIAL_AWARDS, None)
    for tweet in tweets_containing_present:
        #if re.search("([A-Za-z]+[\s-]?[A-Za-z]+(and)?)+\spresent", tweet):
        #if re.search(" [A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[a-z][a-z\-]+){0,1}\s+[A-Z]([a-z]+|\.)", tweet):
        pattern1 = re.search("([A-Z][a-z]*)[\s-]([A-Z][a-z]*)[\s-](and)[\s-]([A-Z][a-z]*)[\s-]([A-Z][a-z]*)", tweet)
        pattern2 = re.search("[A-Z]([a-z]+|\.)(?:\s+[A-Z]([a-z]+|\.))*(?:\s+[A-Z][a-z\-]+){0,1}\s+[A-Z]([a-z]+|\.)", tweet)
        pattern3 = re.search(r'\bbest\s+([^.!?@:#-]*)', tweet, re.IGNORECASE)
        presenters = []
        if "Halle Berry" in tweet:
            print(tweet)
        if pattern1 and pattern3:
            name1 = pattern1.group(1) + ' ' + pattern1.group(2)
            name2 = pattern1.group(4) + ' ' + pattern1.group(5)
            presenters.append(name1)
            presenters.append(name2)
        elif pattern2 and pattern3:
            name1 = pattern2.group(0)
            name2 = pattern2.group(2)
            check = [word for word in name1 if word.lower() in nltk_stop_words or word.lower() in award_stop_words]
            if not check:
                presenters.append(name1)
        if presenters:
            highest = 0
            mapping = ''
            for award in OFFICIAL_AWARDS:
                seq = SequenceMatcher(None, award, pattern3.group(0))
                ratio = seq.ratio()
                #ratio = Levenshtein.ratio(award,pattern3.group(0))
                if ratio > highest:
                    highest = ratio
                    mapping = award
            if highest >= .4:
                for presenter in presenters:
                    if not awards[mapping]:
                        awards[mapping] = Counter()
                    if presenter in awards[mapping]:
                        awards[mapping][presenter] += 1
                    else:
                        awards[mapping][presenter] = 1

    result = dict.fromkeys(OFFICIAL_AWARDS,None)
    print(awards)
    for key in awards:
        #print(awards[key])
        if awards[key]:
            targets = awards[key].most_common(2)
            res = []
            for i in targets:
                res.append(i[0])
            result[key] = res
        else:
            result[key] = []
    return result


def get_presenters_2(year):
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
            check = [word for word in name1 if word.lower() in nltk_stop_words or word.lower() in award_stop_words]
            if not check:
                presenters_tweets.append(name1)
    presenters = Counter()
    presenters.update(presenters_tweets)
    possible_presenters = list(set(presenters.keys()))
    possible_presenters.remove("Golden Globes")
    return map_presenters(2013, possible_presenters)
  
def map_presenters(year, presenters):
    awards = dict.fromkeys(OFFICIAL_AWARDS, None)
    best_pattern = re.compile(r"\bbest\s+([^.!?@:/'()-]*)")
    tweets_containing_best = list(filter(best_pattern.search, get_tweets(year)))
    for tweet in tweets_containing_best:
        matches = [presenter for presenter in presenters if(presenter in tweet)]
        if matches:
            if best_pattern.search(tweet):
                highest = 0
                mapping = ''
                match = best_pattern.search(tweet)
                for award in OFFICIAL_AWARDS:
                    seq = SequenceMatcher(None, award, match.group(0))
                    ratio = seq.ratio()
                    if ratio > highest:
                        highest = ratio
                        mapping = award
                if highest >= .4:
                    for presenter in matches:
                        #print(presenter)
                        if not awards[mapping]:
                            awards[mapping] = Counter()
                        if presenter in awards[mapping]:
                            awards[mapping][presenter] += 1
                        else:
                            awards[mapping][presenter] = 1
    result = dict.fromkeys(OFFICIAL_AWARDS,None)
    for key in awards:
        #print(awards[key])
        if awards[key]:
            targets = awards[key].most_common(2)
            res = []
            for i in targets:
                res.append(i[0])
            result[key] = res
        else:
            result[key] = []
    return result
                


            
   


get_presenters(2013)
#map_presenters(2013)
#get_presenters_1(2013)