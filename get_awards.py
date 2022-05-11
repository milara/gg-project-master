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
    award_discussion_pattern1 = re.compile('(gets|got)(.*)')
    award_tweets = []


    ##### structure: Name (wins) Award
    for tweet in award_mention_tweets:
        result = award_discussion_pattern.search(tweet)

        #########################new add######################
        if not result:
            result = award_discussion_pattern1.search(tweet)
        #########################new add######################

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

            ################new add##########################
            words = substring.split()
            # print(substring)
            if substring[3:].lower() != "best":
                if words and (words[0] == "#GoldenGlobe" and words[1] == "for"):
                    words = words[2:]
                    substring = ' '.join(words)
                    # for i in range(len(words)):
                    #     substring = ' '.join(words[:i])
                elif words and  len(words)>= 3 and (words[0] == "Golden" and words[1] == "Globe" and words[2] == "for"):
                    words = words[3:]
                    substring = ' '.join(words)
                    # for i in range(len(words)):
                    #     substring = ' '.join(words[:i])
            index = 0
            words = substring.split()
            if "for" in words:
                for i in range(len(words)):
                    if words[i] == "for":
                        index = i
                        break
                words = words[:index]
            substring = ' '.join(words)
            ####################new add##########################
               
            # print(substring)
                    # break

            ######################new add##########################
            award_mention_tweets.remove(tweet)  
            ####new add####
                    
            award_tweets.append(substring)
    
    award_discussion_pattern2 = re.compile('(.*)(goes to|is awarded to)')

    for tweet in award_mention_tweets:
        result = award_discussion_pattern2.search(tweet)

        if result:
            substring = result.group(0).strip().lower()
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
                # words = substring.split()
                # words = words[:-8]
                # substring = ' '.join(words)
                substring = substring[:-8]
            elif "is awarded to" in substring:
                # words = substring.split()
                # words = words[:-14]
                # substring = ' '.join(words)
                substring = substring[:-14]
            print(substring)
            award_tweets.append(substring)


            # if words and (words[0] == "for" or words[0] == "the"):
            #     words.pop(0)
            #     for i in range(len(words)):
            #         # print(words[i])
            #         if words[i] != ',':
            #             substring = ' '.join(words[:i])
                      #  # break

            # ################new add##########################
            # words = substring.split()
            # # print(substring)
            # if substring[3:].lower() != "best":
            #     if words and (words[0] == "#GoldenGlobe" and words[1] == "for"):
            #         words = words[2:]
            #         substring = ' '.join(words)
            #         # for i in range(len(words)):
            #         #     substring = ' '.join(words[:i])
            #     elif words and  len(words)>= 3 and (words[0] == "Golden" and words[1] == "Globe" and words[2] == "for"):
            #         words = words[3:]
            #         substring = ' '.join(words)
            #         # for i in range(len(words)):
            #         #     substring = ' '.join(words[:i])
            # index = 0
            # words = substring.split()
            # if "for" in words:
            #     for i in range(len(words)):
            #         if words[i] == "for":
            #             index = i
            #             break
            #     words = words[:index]
            # ####################new add##########################
               
            # #print(substring)
            #         # break

            # ######################new add##########################
            # award_mention_tweets.remove(tweet)  
            # ####new add####
                    
            # award_tweets.append(substring)






    
    # print("original corpus length:", len(award_mention_tweets))
    # print("award tweets length:", len(award_tweets))




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