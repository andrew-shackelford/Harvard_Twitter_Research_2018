'''
Use existing architecture from twitter_hashtag_filter to get users by searching
their name on twitter and filter by verified users. Store these user objects
in a json file. Implemented to get user profiles of all midterm election
candidates.

Usage example:

Use Hailey's Twitter API keys to get all the handles from the the first 200
candidates listed in names_part_1.txt (copied from the spreadsheet)

python twitter_user_handles.py ConfigFiles/handles/hailey_part_1.txt
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

    # with open(out_dir + "/" + out_file + '.json', 'a') as outFile: # entire user object
    with open(out_dir + '/candidate_handles.txt', 'a') as outFile: # handle only
        for name in data.split(','):
            if name != '':
                query = name + '& filter:verified'
                users = api.search_users(q=name)
                if len(users) > 0:
                    user = users[0]
                    outFile.write('@' + user.screen_name + '\n') # handle only
                    # json.dump(user._json, outFile) # entire user object
