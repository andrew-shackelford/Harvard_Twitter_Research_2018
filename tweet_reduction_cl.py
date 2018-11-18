import json, os, pickle

class tweet_tags(object):

    def __init__(self, jl_line):
        '''
        Initialize the data fields in the object, taken from a json line
        :param jl_line: parsed line of the tweet
        '''
        self.id = jl_line['id_str']
        self.tweeter_id = jl_line['user']['id_str']
        self.hashtags = jl_line['entities']['hashtags']
        self.geo_tag = jl_line['coordinates']
        if 'retweeted_status' in jl_line:
            self.retweet = jl_line['retweeted_status']
        else:
            self.retweet = None
        self.retweet_count = jl_line['retweet_count']

class tweeter(object):

    def __init__(self, jl_line):
        '''
        Initializes the data for an object representation of someone/something that tweets
        :param jl_line:
        '''
        self.id = jl_line['user']['id_str']
        self.followers_count= jl_line['user']['followers_count']
        self.friends_count = jl_line['user']['friends_count']
        self.tweet_count = 1

    def incr_tweet_count(self):
        self.tweet_count += 1

