import json
import re
from collections import Counter
import nltk
nltk.download('stopwords')

def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            tweet_text_lst.append(tweet['text'])

    return tweet_text_lst

# TODO: "AWARD" goes to ...
# Cut end of tweet
def get_award(year):
    # Parse through tweets to find "[Bb]est" within the titles

    award_best_pattern = re.compile('[Bb]est')
    award_mention_tweets = list(filter(award_best_pattern.search, get_tweets(year)))

    award_discussion_pattern = re.compile('(wins|won|is awarded)(.*)')
    award_discussion_pattern1 = re.compile('(gets|got)(.*)')
    award_discussion_pattern2 = re.compile('(.*)(goes to|is awarded to)')
    award_tweets = []


    ##### structure: Name (wins) Award
    for tweet in award_mention_tweets[:]:
        result = award_discussion_pattern.search(tweet)
        result2 = award_discussion_pattern2.search(tweet)

        if not result:
            result = award_discussion_pattern1.search(tweet)
        if result:
            substring = result.group(2).strip().lower()
            #########################new add######################
            #substring = re.sub(r'[^\w\s]', '', substring)
            ##########################
            words = nltk.word_tokenize(substring)
            words = substring.split()
            #print(words)
            if words and (words[0] == "for" or words[0] == "the"):
                words.pop(0)
                for i in range(len(words)):
                    # print(words[i])
                    if words[i] != ',':
                        substring = ' '.join(words[:i])
                #         break
            words = substring.split()

            if substring[3:].lower() != "best":
                if words and (words[0] == "#GoldenGlobe" and words[1] == "for"):
                    words = words[2:]
                    substring = ' '.join(words)
                elif words and  len(words)>= 3 and (words[0] == "Golden" and words[1] == "Globe" and words[2] == "for"):
                    words = words[3:]
                    substring = ' '.join(words)
            index = 0
            words = substring.split()
            if "for" in words:
                for i in range(len(words)):
                    if words[i] == "for":
                        index = i
                        break
                words = words[:index]
            substring = ' '.join(words)

            # award_mention_tweets.remove(tweet)  
            # print(substring)
            award_tweets.append(substring)

        elif result2:   
            substring = result2.group(0).strip().lower()
            words = nltk.word_tokenize(substring)
            words = substring.split()
            id = 0
            for i in range(len(words)):
                if words[i].lower() == "best":
                    del words[:i]
                    break
            if words[0] == "rt":
                del words[:2]
            substring = ' '.join(words)
            if "goes to" in substring:
                substring = substring[:-8]
            elif "is awarded to" in substring:
                substring = substring[:-14]
            # print(substring)
            award_tweets.append(substring)
            # if "golden globe" in substring:
                

    awards = Counter()
    awards.update(award_tweets)
    return awards.most_common(40)

# print('2013: ', get_award('2013'))
# print('2015: ', get_award('2015'))