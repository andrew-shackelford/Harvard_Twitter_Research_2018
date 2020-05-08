#!/usr/bin/evn python3
# -*- coding: utf-8 -*-
"""
Created on 4/29/20

@author waldo

Objects used to store a reduced set of information about a tweet. The tweet object is the basic for this group,
storing the tweet id, text, and hashtags. If the tweet is a quote or a retweet, a tweet object of the tweet
that is quoted or retweeted is also stored. A user object is also stored, showing who tweeted this.
"""

class tweet(object):
    """
    A basic tweet object. Holds the tweet_id, text, any hashtags, mentions,
    a user object, and different information for retweets, quotes, and replies.
    """
    def __init__(self, js_tweet):
        self.tweet_id = js_tweet['id_str']
        self.text = js_tweet['text']
        if 'entities' in js_tweet:
            self.hashtags = []
            for h in js_tweet['entities']['hashtags']:
                self.hashtags.append(h['text'])
            self.mentions = js_tweet['entities']['user_mentions']
        self.user = tweet_user(js_tweet['user'])
        
        if 'retweeted_status' in js_tweet:
            self.retweet = tweet(js_tweet['retweeted_status'])
            self.retweet_count = js_tweet['retweet_count']
        else:
            self.is_retweet = ''
        if js_tweet['in_reply_to_status_id_str'] != None :
            self.in_reply = t_reply(js_tweet)
        else:
            self.in_reply = ''
        if js_tweet['is_quote_status'] and 'quoted_status' in js_tweet:
            self.quote = tweet(js_tweet['quoted_status'])
        else:
            self.quote = None
        self.quote_status = js_tweet['is_quote_status']

class tweet_user(object):
    """
    A user object. Holds information about the user who issued a tweet, including
    the screen name, user_id, location, description, followers and friends count,
    and if the account is verified.
    """
    def __init__(self, js_user):
        self.screen_name = js_user['name']
        self.user_id = js_user['id_str']
        self.followers_count = js_user['followers_count']
        self.friends_count = js_user['friends_count']
        self.verified = js_user['verified']

class t_reply(object):
    """
    A tweet reply object, holding information relevant only to a reply, including
    the id, author id, and author screen name of the tweet being replied to.
    """
    def __init__(self, js_tweet):
        self.original_id = js_tweet['in_reply_to_status_id_str']
        self.author_id = js_tweet['in_reply_to_user_id_str']
        self.author_screen_name = js_tweet['in_reply_to_screen_name']




