import json
import re
from os.path import exists

'''
PREPROCESSES TWEETS

JSON of Tweets => TXT file, line delimited of cleaned Tweet strings
Currently I've just been testing it and reading processed data into a .txt file through cmd line
As you can see in beginning of function, we can also store it in a .txt and read from it 
(as to not process tweets over and over again, processing takes a few seconds)
'''

HASHTAG_DIC = {}
MENTION_DIC = {}

def get_tweets(year):
    if exists('processedtweets{}.txt'.format(year)):
        return open('processedtweets{}.txt'.format(year)).readlines()

    with open('../gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []

        for tweet in tweet_information:
            tweet = tweet['text']
            tweet = clean(tweet)
            tweet_text_lst.append(tweet)

    for i, tweet in enumerate(tweet_text_lst):
        tweet_text_lst[i] = separateHashtags(tweet_text_lst[i])
        tweet_text_lst[i] = fixMentions(tweet_text_lst[i])

        ''' 
        this next line surrounds every punctuation and other 'useless' character with spaces
        this would let a dumber algorithm match names or other keywords better, and furthermore
        i dont think we care about punctuation (doing this wouldn't affect anything, right?)

        e.g. "Leo DiCaprio's" => "Leo DiCaprio ' s"
        '''
        tweet_text_lst[i] = re.sub('([^a-zA-Z0-9\s])', r' \1 ', tweet_text_lst[i]) 

        tweet_text_lst[i] = re.sub('\s+', ' ', tweet_text_lst[i])
        if re.match('\s+', tweet_text_lst[i]):
            tweet_text_lst[i] = re.sub('\s+', '', tweet_text_lst[i], 1)

    return tweet_text_lst

def clean(text):
    text = re.sub('&amp;', " and ", text)
    text = re.sub('(&gt;)+', ' are greater than ', text)
    text = re.sub('(&lt;3+)+', ' heartemote ', text)
    text = re.sub('(&lt;)+', " are less than ", text)
    text = re.sub(':\(+', ' frownemote ', text)
    text = re.sub(':\)+', ' smileemote ', text)
    text = re.sub('\s+', ' ', text)
    text = removeRT(text)
    text = removeLinks(text)
    text = separateHashtags(text)
    text = fixMentions(text)
    return text

def removeRT(text):
    rt = re.compile(r'RT @[a-zA-Z0-9_-]+(:?)\s')
    if re.search(rt, text) or re.match(rt, text):
        return re.sub(rt, "", text)
    return text

def removeLinks(text):
    link = re.compile('http(s?)\S*')
    if re.search(link, text):
        return re.sub(link, "", text)
    return text

def separateHashtags(text):
    hashtags = re.findall("#[a-zA-Z]*", text)
    for h in hashtags:
        if h.lower() in HASHTAG_DIC:
            text = re.sub(h, HASHTAG_DIC[h.lower()], text)
        elif h != h.lower():
            trans = re.sub(r'(?<!^)(?=[A-Z])', ' ', h)[1:]
            text = re.sub(h, trans, text)
            HASHTAG_DIC[h.lower()] = trans.lower()
    return text

def fixMentions(text):
    ats = re.findall("@[a-zA-Z0-9_]+", text)
    for a in ats:
        if a.lower() in MENTION_DIC:
            text = re.sub(a, MENTION_DIC[a.lower()], text)
        elif a != a.lower():
            trans = re.sub(r'(?<!^)(?=[A-Z])', ' ', a)[1:]
            trans = re.sub('\s*_\s*', ' ', trans)
            trans = re.sub('[0-9]*', '', trans)
            text = re.sub(a, trans, text)
            MENTION_DIC[a.lower()] = trans.lower()
    return text


#UNCOMMENT ME FOR TESTING "python3 tweet_preprocessing.py > tweets2013.txt"
for line in get_tweets(2013):
     print(line)
