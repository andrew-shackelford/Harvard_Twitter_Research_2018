import os
import pickle
import sys

class User_Analyzer:

    def __init__(self):
        pass

    def analyze_user_file(self, infile, data={}):
        '''
        Analyze the date of tweets by user from a pickle file of scraped tweets.
        :param infile: The filename of the pickle file to be parsed
        :return: A list of dictionaries (each dictionary represents a user's tweets).
        '''
        if (infile[-4:] != ".pkl"):
            print(infile + " is of invalid type.")
            return []
        
        try:
            sys.stdout.write("analyzing " + infile + "...")
            sys.stdout.flush()

            with open(infile) as f:
                tweets = pickle.load(f)

            for tweet in tweets:
                if not tweet['retweeted']:
                    user_id = tweet['user']['id']
                    date = tweet['created_at']

                    if user_id not in data:
                        data[user_id] = {}
                        data[user_id]['screen_name'] = tweet['user']['screen_name']
                        data[user_id]['full_name'] = tweet['user']['name']
                        data[user_id]['count'] = 0
                        data[user_id]['tweet_dates'] = []

                    data[user_id]['count'] = data[user_id]['count'] + 1
                    data[user_id]['tweet_dates'].append(tweet['created_at'])
                
            print("done")
        except:
            print("FAILED")
            return []

        return data

    def analyze_user_folder(self, infolder):
        '''
        Analyze the date of tweets by user form a folder filled with pickle files of scraped tweets.
        :param infile: The folder containing the pickle files to be parsed
        :return: A list of dictionaries (each dictionary represents a user's tweets).
        '''
        all_data = {}
        for file in os.listdir(infolder):
            if (file[-4:] == ".pkl"):
                all_data = self.parse_json_file(file, all_data)
        return all_data