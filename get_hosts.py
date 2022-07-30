import json
import re
from collections import Counter

def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            tweet_text_lst.append(tweet['text'])

    return tweet_text_lst

def get_hosts(year):
    host_discussion_pattern = re.compile('hosted|hosting')
    host_relevant_tweets = list(filter(host_discussion_pattern.search, get_tweets(year)))

    host_multiple_names_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+ (and|&) [A-Z][a-z]+ [A-Z][a-z]+')
    host_mention_tweets = list(filter(host_multiple_names_pattern.search, host_relevant_tweets))

    host_name_pattern = re.compile('[A-Z][a-z]+ [A-Z][a-z]+')
    host_names = Counter()
    for tweet in host_mention_tweets:
        potential_names = host_name_pattern.findall(tweet)
        host_names.update(potential_names)
    
    hosts = []
    lstofhosts = host_names.most_common(2)
    for n,f in lstofhosts:
        hosts.append(n)
    return hosts

print('2013: ', get_hosts('2013'))
print('2015: ', get_hosts('2015'))