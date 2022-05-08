import json
import re
from collections import Counter
import nltk

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
    # wins, wins the award for, won, won the award for, is awarded, wins for, won for, gets the award for, got the award for, gets, got

    # Parse through tweets to find "[Bb]est" within the titles
    award_best_pattern = re.compile('[Bb]est')
    award_mention_tweets = list(filter(award_best_pattern.search, get_tweets(year)))

    award_discussion_pattern = re.compile('(wins|won|is awarded)(.*)')
    award_tweets = []

    for tweet in award_mention_tweets:
        result = award_discussion_pattern.search(tweet)
        if result:
            substring = result.group(2).strip()
            break
            words = nltk.word_tokenize(substring)
            # words = substring.split()
            # print(words)
            # if words and (words[0] == "for" or words[0] == "the"):
            #     words.pop(0)
            #     for i in range(len(words)):
            #         print(words[i])
            #         if words[i] != ',':
            #             substring = ' '.join(words[:i])
            #             break
            #     break
                        
            # award_tweets.append(substring)

    # print(award_tweets)
    
    # print(all_tweets)
    # award_relevant_tweets = list(filter(award_discussion_pattern.search, get_tweets(year)))
    # print(award_relevant_tweets)
    # for i, tweet in enumerate(award_relevant_tweets):
        # print(award_relevant_tweets[i].groups())
        # break
        #award_relevant_tweets[i] = tweet.group(1)
    # print(award_relevant_tweets)

    # First parse through all the tweets for wins|won etc (structure = Name (wins|won|etc) Award)

    # # Filter through those to find "for"
    

    # # Take substrings between "Best" and "for" -> award

    
    # award_name_pattern = re.compile('wins(.*)for')
    # award_names = Counter()
    # for tweet in award_relevant_tweets:
    #     potential_awards = award_name_pattern.search(tweet)
    #     print(potential_awards.group(1))
    #     break
    #     award_names.update(potential_awards)
    
    # hosts = []
    # lstofhosts = host_names.most_common(2)
    # for n,f in lstofhosts:
    #     hosts.append(n)
    #return 0

print('2013: ', get_award('2013'))
# print('2015: ', get_hosts('2015'))