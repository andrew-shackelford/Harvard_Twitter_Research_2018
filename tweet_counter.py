import csv
import sys

class Tweet_Counter:
    def __init__(self):
        pass

    def count_tweets_file(self, infile, data={}):
        print("analyzing " + infile + "...")
        with open(infile, 'rb') as in_csv:
            reader = csv.reader(in_csv)
            for tweet in reader:
                user_id = tweet[1]
                data[user_id] = data.get(user_id, 0) + 1

        return data

    def count_tweets_folder(self, infolder, data={}):
        for file in os.listdir(infolder):
            if file[-4:] == '.csv':
                data = self.count_tweets_file(infolder + file, data)
        return data