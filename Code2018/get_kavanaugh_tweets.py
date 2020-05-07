'''
This script will take json files of tweets in the directory and copy
tweets that include pro/anti-Kavanaugh hashtags to a new file
'''
import json
import os

kavanaugh_hashtags = set([
    'confirmkavanaugh',
    'confirmkavanaughnow',
    'voteredtosaveamerica',
    'confirmbrettkavanaugh',
    'comfirmkavanaugh',
    'confirmjudgekavanaughnow',
    'istandwithkavanaugh',
    'takethevote',
    'standwithkavanaugh',
    'confirmjudgekavanaugh',
    'confirmbrettkavanaughnow',
    'himtookavanaughforscotus',
    'comfirmkavanaughnow',
    'istandwithbrett',
    'prayforjudgekavanaugh',
    'assaultisneverokay',
    'believesurvivors',
    'kavano',
    'metoo',
    'stopkavanaugh',
    'voteno',
    'justicenow',
    'blockkavanaugh',
    'kavanope',
    'nokavanaugh',
    'believesurvivors',
    'nokavanaughconfirmation'
])

dir = os.listdir('..')
for file_name in dir:
    print(file_name)
    outfile_name = 'kavanaugh' + file_name[3:]
    with open(file_name, 'r') as infile, open(outfile_name, 'w') as outfile:
        for line in infile:
            if line != None:
                tweet = json.loads(line.rstrip('\n'))
                try:
                    hashtags_in_tweet = set([hashtag['text'] for hashtag in tweet['entities']['hashtags']])
                    if len(kavanaugh_hashtags.intersection(hashtags_in_tweet)):
                        outfile.write(json.dumps(tweet))
                except:
                    print(tweet)
