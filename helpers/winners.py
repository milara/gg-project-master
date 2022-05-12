import json
import re
import nltk
from collections import Counter
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

award_stop_words = set(['by', 'an', 'in', 'a', 'performance', 'or', 'role', 'made', 'for', '-', ','])
nltk_stop_words = set(stopwords.words('english'))
nltk_stop_words.update(['http', 'golden', 'globes', 'goldenglobes', 'goldenglobe'])

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

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
            text_lst = nltk.tokenize.word_tokenize(tweet['text'])
            filtered_text_lst = [token for token in text_lst if token.lower() not in nltk_stop_words and token.isalpha()]
            if filtered_text_lst and filtered_text_lst[0] == 'RT':
                del filtered_text_lst[0:2]
            tweet_text_lst.append(' '.join(filtered_text_lst))
            # print(' '.join(filtered_text_lst))

    return tweet_text_lst

# https://stackoverflow.com/questions/24398536/named-entity-recognition-with-regular-expression-nltk
def get_continuous_chunks(text):
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    if current_chunk:
        named_entity = " ".join(current_chunk)
        if named_entity not in continuous_chunk:
            continuous_chunk.append(named_entity)
            current_chunk = []
    return continuous_chunk

def get_winner(year):
    award_mappings = get_filtered_awards(year)
    
    potential_winners = {}
    for clean_award in award_mappings.keys():
        potential_winners[clean_award] = Counter()

    won_pattern = re.compile('goes to|got|won|wins|is awarded')
    tweets_containing_won = list(filter(won_pattern.search, get_tweets(year)))
    
    for tweet in tweets_containing_won:
        splitted_tweet = tweet.split()

        for clean_award in award_mappings.keys():
            if len(clean_award.intersection(set(splitted_tweet))) / len(clean_award) >= 0.75:
                # print(tweet)
                # print(get_continuous_chunks(tweet))
                potential_winners[clean_award].update(get_continuous_chunks(tweet))

    winners = {}
    for award in potential_winners.keys():
        award_name = award_mappings[award]
        print("AWARD={}, POTENTIAL_WINNERS={}".format(award_mappings[award], potential_winners[award].most_common(10)))
        if len(potential_winners[award]) > 0:
            winners[award_name] = potential_winners[award].most_common(1)[0][0]
        else:
            winners[award_name] = "Not found"

    return winners

# Returns dictionary mapping between KEY = clean name, VALUE = original name
def get_filtered_awards(year):
    clean_awards = {}
    for award in OFFICIAL_AWARDS:
        text_lst = nltk.tokenize.word_tokenize(award)
        filtered_text_lst = [token for token in text_lst if token not in award_stop_words]
        clean_awards[frozenset(filtered_text_lst)] = award
        # print("AWARD: {}, list: {}".format(award, filtered_text_lst))

    return clean_awards


# get_filtered_awards('2013')
# get_winner('2013')
# print(get_continuous_chunks('john doe wins THE award'))
