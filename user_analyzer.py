import os
import json
import pickle
from datetime import datetime

class User_Analyzer:

    def __init__(self):
        pass

    def __analyze_user_json(self, infile, data):
        print("analyzing " + infile + "...")

        with open(infile) as f:
            for line in f:
                try:
                    tweet = json.loads(line)
                    if not tweet['retweeted']:
                        user_id = tweet['user']['id']
                        if user_id not in data:
                            data[user_id] = {}
                            data[user_id]['screen_name'] = tweet['user']['screen_name']
                            data[user_id]['full_name'] = tweet['user']['name']
                            data[user_id]['count'] = 0
                            data[user_id]['tweet_dates'] = []
                            data[user_id]['tweet_times'] = {}

                        time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                        hours = int(round((time - datetime(2018,1,1)).total_seconds() / 3600))

                        data[user_id]['count'] = data[user_id]['count'] + 1
                        data[user_id]['tweet_dates'].append(tweet['created_at'])
                        data[user_id]['tweet_times'][hours] = data[user_id]['tweet_times'].get(hours, 0) + 1
                except:
                    print("tweet failed")

        print("analyzing done")

        return data

    def __analyze_user_pkl(self, infile, data):
        print("analyzing " + infile + "...")

        with open(infile) as f:
            tweets = pickle.load(f)

        for tweet in tweets:
            try:
                if not tweet['retweeted']:
                    user_id = tweet['user']['id']
                    if user_id not in data:
                        data[user_id] = {}
                        data[user_id]['screen_name'] = tweet['user']['screen_name']
                        data[user_id]['full_name'] = tweet['user']['name']
                        data[user_id]['count'] = 0
                        data[user_id]['tweet_dates'] = []
                        data[user_id]['tweet_times'] = {}

                    time = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
                    hours = int(round((time - datetime(2018,1,1)).total_seconds() / 3600))

                    data[user_id]['count'] = data[user_id]['count'] + 1
                    data[user_id]['tweet_dates'].append(tweet['created_at'])
                    data[user_id]['tweet_times'][hours] = data[user_id]['tweet_times'].get(hours, 0) + 1
            except:
                print("tweet failed")
        print("analyzing done")

        return data

    def analyze_user_file(self, infile, data={}):
        '''
        Analyze the date of tweets by user from a json or pickle file of scraped tweets.
        :param infile: The filename of the json or pickle file to be parsed
        :param data (optional): an optional dictionary of data to append to
        :return: A list of dictionaries (each dictionary represents a user's tweets).
        '''
        if infile[-4:] == ".pkl":
            return self.__analyze_user_pkl(infile, data)
        elif infile[-5:] == ".json":
            return self.__analyze_user_json(infile, data)
        else:
            print(infile + " is of invalid type.")
            return []

        return data

    def analyze_user_folder(self, infolder):
        '''
        Analyze the date of tweets by user from a folder filled with pickle or json files of scraped tweets.
        :param infile: The folder containing the pickle/json files to be parsed
        :return: A list of dictionaries (each dictionary represents a user's tweets).
        '''
        all_data = {}
        for file in os.listdir(infolder):
            if file[-4:] == ".pkl":
                all_data = self.__analyze_user_pkl(infolder + file, all_data)
            elif file[-5:] == ".json":
                all_data = self.__analyze_user_json(infolder + file, all_data)
        return all_data