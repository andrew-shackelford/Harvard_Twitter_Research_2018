import json, os, pickle


class tweet_tags(object):

    def __init__(self, jl_line):
        '''
        Initialize the data fields in the object, taken from a json line. Currently we take the id of the tweet, user id,
        user name, a list of hashtags, the geo-coordinates, and the retweet status, retweet count, favorite count, reply
        count, and quote count
        :param jl_line: parsed line of the tweet
        '''
        self.id = jl_line['id_str']
        self.tweeter_id = jl_line['user']['id_str']
        self.user_name = jl_line['user']['screen_name']
        self.hashtags = []
        for h in jl_line['entities']['hashtags']:
            self.hashtags.append(h['text'])
        self.geo_tag = jl_line['coordinates']
        if 'retweeted_status' in jl_line:
            self.retweet = jl_line['retweeted_status']['id_str']
        else:
            self.retweet = None
        self.retweet_count = jl_line['retweet_count']
        self.favorite_count = jl_line['favorite_count']
        self.reply_count = jl_line['reply_count']
        self.quote_count = jl_line['quote_count']

    def get_values_as_list(self):
        '''
        Return the values stored in the object as a list, ready to be written to a .csv file
        :return: A list of the values stored in the object.
        '''
        return [self.id, self.tweeter_id, self.user_name, self.hashtags, self.geo_tag, self.retweet, self.retweet_count,
                self.favorite_count, self.reply_count, self.quote_count]


class tweeter(object):

    def __init__(self, jl_line):
        '''
        Initializes the data for an object representation of someone/something that tweets
        :param jl_line:
        '''
        self.id = jl_line['user']['id_str']
        self.followers_count = jl_line['user']['followers_count']
        self.friends_count = jl_line['user']['friends_count']
        self.tweet_count = 1

    def incr_tweet_count(self):
        self.tweet_count += 1

    def get_values_as_list(self):
        return [self.id, self.followers_count, self.friends_count, self.tweet_count]
