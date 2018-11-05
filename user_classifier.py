from __future__ import print_function
import os
import json
import pickle
from datetime import datetime

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class User_Classifier:

    def __init__(self):
        pass

    def classify_users(self, infile, num_tweets=10):
        print("loading users from " + infile + "...")

        # load data from file
        with open(infile, 'rb') as f:
            users = pickle.load(f)

        for user_id, user in users.iteritems():
            try:
                # skip tweets we've already classified
                if 'classification' in user:
                    continue

                # ensure minimum number of tweets
                length = len(user['tweets'])
                if length < num_tweets:
                    continue

                idx = 0

                while True:
                    tweet = user['tweets'][idx]

                    # print user details
                    os.system('clear')
                    print("user_id is " + str(user_id))
                    print("screen_name is " + bcolors.OKGREEN + user['screen_name'] + bcolors.ENDC)
                    print("full_name is " + bcolors.OKBLUE + user['full_name'] + bcolors.ENDC)
                    print()

                    # print user's tweeting frequencies
                    print("frequencies are: ")
                    print(bcolors.HEADER, end="")
                    hours = sorted(user['tweet_times'].keys())
                    for hour in hours:
                        val = user['tweet_times'][hour]
                        print(str(hour) + ": ", end="")
                        print(str(val) + ", ", end="")
                    print(bcolors.ENDC)
                    print()

                    # print tweet
                    print(bcolors.WARNING + "tweet " + str(idx+1) + " of " + str(length) + bcolors.ENDC)
                    print()
                    print(bcolors.FAIL + tweet + bcolors.ENDC)
                    print()
                    print(bcolors.BOLD + "Enter \'b\' to label as bot, \'p\' as person, \'?\' as unknown, \'c\' to display the next tweet from this user, \'x\' for previous, and \'q\' to stop labeling for now" + bcolors.ENDC)
                    print()

                    # handle input
                    result = raw_input()
                    if result == 'c':
                        idx = min(idx+1, length-1)
                    elif result == 'x':
                        idx = max(idx-1, 0)
                    elif result == '':
                        pass
                    else:
                        break

                # quit labeling
                if result == 'q':
                    break

                user['classification'] = result

            except:
                print("user failed")

        # write out to file
        with open(infile, 'wb') as f:
            print("writing out to file")
            pickle.dump(users, f)

        print("classifications written out to file")
