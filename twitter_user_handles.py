'''
Use existing architecture from twitter_hashtag_filter to get users by searching
their name on twitter and filtering by verified users. Store these user objects
in a json file. Currently used to get user profiles of all midterm election
candidates.
'''
import tweepy
import twitter_hashtag_filter as thf
import sys
import json

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python twitter_user_handles.py config_file_name')
        sys.exit(1)

    fname = sys.argv[1]
    config = thf.read_config_file(fname)

    auth = thf.make_auth(config)
    api = tweepy.API(auth)

    data = thf.get_filter_list(config)

    if 'output_directory' in config:
        out_dir = config['output_directory']
    else:
        out_dir = '.'

    if 'output_file' in config:
        out_file = config['output_file']
    else:
        out_file = 'test_output'

    if data == '':
        print('No names specified for finding handles, program exiting')
        sys.exit(1)

# Search each name, and write the first found verified user to the output json file

    with open(out_dir + "/" + out_file + '.json', 'a') as outFile:
        for name in data.split(','):
            if name != '':
                query = name + '& filter:verified'
                users = api.search_users(q=name)
                if len(users) > 0:
                    user = users[0]
                    json.dump(user._json, outFile)
