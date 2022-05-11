import json
import re
import nltk
from collections import Counter
from difflib import SequenceMatcher
# from nltk.corpus import stopwords

# stop_words = set(stopwords.words('english'))

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def similiar(a,b):
    if SequenceMatcher(None, a, b).ratio() >= 0.70:
        return True
    else:
        return False

# Returns all tweet text from year in lowercase without stop words
def get_tweets(year):
    with open('gg{}.json'.format(year)) as f:
        tweet_information = json.load(f)

        tweet_text_lst = []
        for tweet in tweet_information:
            # lowered_text = tweet['text'].lower()
            # text_lst = nltk.tokenize.word_tokenize(lowered_text)
            # filtered_text_lst = [token for token in text_lst if token not in stop_words]
            # tweet_text_lst.append(' '.join(filtered_text_lst))
            tweet_text_lst.append(tweet['text'])

    return tweet_text_lst

def get_winner(year):
    if year == '2013':
        award_mappings = {}
        with open('./2013categories.txt') as file:
            lines = file.readlines()
            for line in lines:
                award_mappings[line] = None
    
    all_tweets = get_tweets(year)
    potential_winners = {}
    for award in award_mappings.keys():
        potential_winners[award] = Counter()

    won_pattern = re.compile('got|won|wins|is awarded')
    tweets_containing_won = list(filter(won_pattern.search, get_tweets(year)))
    
    for tweet in tweets_containing_won:
        splitted_tweet = won_pattern.split(tweet)
        potential_winner = splitted_tweet[0]
        potential_award = splitted_tweet[1]

        for award in award_mappings.keys():
            if award in potential_award:   
                splitted_potential_winner = potential_winner.split()             
                # Backwards count from award
                for i in range(len(potential_winner) - 1, 0, -1):
                    temp = ' '.join(splitted_potential_winner[i+1:])
                    potential_winners[award][temp] = potential_winners[award].get(temp, 0) + 1

                # Forwards count to award
                for i in range(len(splitted_potential_winner)):
                    temp = ' '.join(splitted_potential_winner[:i+1])
                    potential_winners[award][temp] = potential_winners[award].get(temp, 0) + 1

    for award in potential_winners.keys():
        print(award, potential_winners[award].most_common(10))
    # for award in award_mappings.keys():
    #     award_mappings[award] = potential_winners[award].most_common(10)

    # return award_mappings

get_winner('2013')
