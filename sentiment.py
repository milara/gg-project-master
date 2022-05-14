from nltk.corpus import stopwords as sw
from nltk.tokenize import wordpunct_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer as lemma
import json
import re
from collections import Counter
from statistics import mean
from textblob import TextBlob
import pandas as pd
import helpers.tweet_preprocessing as tp
import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language

def get_tweets(year):
    # stopwords = sw.words('english')
    # with open('gg{}.json'.format(year)) as f:
    #     tweet_information = json.load(f)

    #     tweet_text_lst = []
    #     for tweet in tweet_information:
    #         tokens = wordpunct_tokenize(tweet['text'])
    #         words = [t for t in tokens if t not in stopwords]
    #         if words[0].lower() == "rt":
    #             del words[2:]
    #         cleantweet = ' '.join(words)
    #         tweet_text_lst.append(cleantweet)

    # return tweet_text_lst
    return tp.get_tweets(year)

def get_answers(year):
    with open('gg{}answers.json'.format(year)) as f:
        answer_information = json.load(f)
    return answer_information

def get_host_answer(year):
    answer_info = get_answers(year)
    hostanswer = answer_info.get("hosts")
    return hostanswer

def get_nominees_answer(year):
    answer_info = get_answers(year)
    nominees = []
    award_data = answer_info.get("award_data")
    for award in award_data:
        info = award_data.get(award)
        lst = info.get("nominees")
        #print(lst)
        nominees.extend(lst)
    return nominees

def get_presenters_answer(year):
    answer_info = get_answers(year)
    presenters = []
    award_data = answer_info.get("award_data")
    for award in award_data:
        info = award_data.get(award)
        lst = info.get("presenters")
        #print(lst)
        presenters.extend(lst)
    return presenters

def get_winners_answer(year):
    answer_info = get_answers(year)
    winners = []
    award_data = answer_info.get("award_data")
    for award in award_data:
        info = award_data.get(award)
        winner = info.get("winner")
        #print(lst)
        winners.append(winner)
    return winners

def detectlang(text):
    @Language.factory("language_detector")
    def get_lang_detector(nlp, name):
        return LanguageDetector()
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe('language_detector', last=True)
    detect_language = nlp(text)._.language
    lang = detect_language.get('language')
    return lang

def get_sentiment(year):
    stopwords = ["golden", "globes", "globe", "goldenglobes", "goldenglobe", "@"]
    alltweets = get_tweets(year)
    hosts = get_host_answer(year)
    # nominees = get_nominees_answer(2013)
    # presenters = get_presenters_answer(2013)
    winners = get_winners_answer(2013)

    def get_adjectives(text):
        blob = TextBlob(text)
        return [word for (word,tag) in blob.tags if tag.startswith("JJ")]
    
    hostsenti = {"hosts": Counter()}
    winnersenti = {}

    for tweet in alltweets:
        
        tweet = tweet.lower()
        tweet = re.sub(r'[^\w\s]', '', tweet)
        
        stopwords = ["golden", "globes", "globe", "goldenglobes", "goldenglobe", "@", 'in', 'an', 'a', 'actress', 'actor',
        'motion', 'picture', 's', 'm', 't', 'best', 'i', 'mejor', 'el','é','o', 'n']

        if hosts[0] in tweet or hosts[1] in tweet:
            hostname1 = hosts[0].split()
            hostname2 = hosts[1].split()
            stopwords.extend([hostname1[0], hostname1[1], hostname2[0], hostname2[1]])
            tokens = wordpunct_tokenize(tweet)
            newtweet = [token for token in tokens if token.lower() not in stopwords]
            cleantweet = " ".join(newtweet)
            adj = get_adjectives(cleantweet)
            #print(cleantweet)
            hostsenti["hosts"].update(adj)
        else:
            for winner in winners:
                if winner not in winnersenti.keys():
                    winnersenti[winner] = Counter()
                name = winner.split()
                # print(name)
                if len(name) == 1 and name[0].lower() in tweet:
                    stopwords.extend(name)
                    # print(stopwords)
                    tokens = wordpunct_tokenize(tweet)
                    newtweet = [token for token in tokens if token.lower() not in stopwords]
                    cleantweet = " ".join(newtweet)
                    adj = get_adjectives(cleantweet)
                    # print(cleantweet, "adj are ", adj)
                    winnersenti[winner].update(adj)
                elif len(name) == 2 and (name[0].lower() in tweet) and (name[1].lower() in tweet):
                    stopwords.extend(name)
                    tokens = wordpunct_tokenize(tweet)
                    newtweet = [token for token in tokens if token.lower() not in stopwords]
                    cleantweet = " ".join(newtweet)
                    adj = get_adjectives(cleantweet)
                    # print(cleantweet, "adj are ", adj)
                    winnersenti[winner].update(adj)
                elif len(name) == 3 and (name[0].lower() in tweet) and (name[1].lower() in tweet) and (name[2].lower() in tweet):
                    stopwords.extend(name)
                    tokens = wordpunct_tokenize(tweet)
                    newtweet = [token for token in tokens if token.lower() not in stopwords]
                    cleantweet = " ".join(newtweet)
                    adj = get_adjectives(cleantweet)
                    # print(cleantweet, "adj are ", adj)
                    winnersenti[winner].update(adj)



    hostsenti["hosts"] = hostsenti["hosts"].most_common(4)
    for winner in winnersenti:
        winnersenti[winner] = winnersenti[winner].most_common(4)
    print(hostsenti)
    print(winnersenti)
                				
get_sentiment(2013)
