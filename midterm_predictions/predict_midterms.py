import json
import pickle
import os
import re
import sys

lib_hashtags = set([ht.lower() for ht in [
    'resist',
    'impeachtrump',
    'p2',
    'bluewave2018'
    'fucktrump',
    'resistance',
    'bluewave',
    'fbr',
    'flipitblue',
    'votebluetosaveamerica',
    'votewithbeto',
    'Votebeto',
    'betofortexas',
    'gopvotingblue',
    'resisttrump',
    'iamawakenow',
    'votethemout2018',
    'votebluetoendthisnightmare',
    'trumplies',
    'trumpliesmatter',
    'goplies',
    'factsmatter',
    'flipthe49th',
    'VoteScholten4Iowa',
    'thisisnotnormal',
    'takeitback',
    'blacklivesmatter',
    'dumptrump',
    'antitrump',
    'protectourcare',
    'votedem',
    'FlipTheHouse',
    'FlipTheSenate',
    'RejectTheNRA',
    'VoteBlue',
    'BlueWave2018',
    'GunSense',
    'flipthe45th',
    'VoteBlueToSaveHealthcare',
    'OpenBorders',
    'VoteBlue2018',
    'CABlueWAVE',
    'VoteBlueThisTuesday',
    'VoteBLUENoMatterWho',
    'Beto4Texas',
    'VoteBlueToSaveAmerica',
    'VoterSuppressionTactics',
    'AbolishIce',
    'Bernie2020',
    'VoterSuppression',
    'VoteForTimCanova',
    'VoteBlueToSaveAmericanDemocracy',
    'VoteJanz',
    'VoteClaire',
    'VoteforAndrewJanz',
    'ReplaceNunes',
    'RepublicanLiars',
    'ResistandWin',
    'medicareforall',
    'freecollege',
    'ObamaLegacy',
    'DemsSoDiverse',
    'FLIPITVOTEBLUE',
    'PreExistingConditions',
    'goodtrouble',
    'REPUBLICUNT',
    'BoycottTysonFoods',
    'StaceyAbrams4GAgov',
    'GunSenseCandidate',
    'TeamAbrams',
    'VoteBlueToSaveAmerica',
    'medicare4all',
    'neonazi',
    'neonazis',
    'whitesupremacist',
    'whitesupremacists',
    'turngablue',
    'prochoice',
    'VoteScholten4Iowa',
    'VoteWalkerOut',
    'LGBT',
    'lgbtq',
    'lgbtq+',
    'GOPTaxScam',
    'LGBTQIA',
    'VoteBlueToSaveDemocracy',
    'VoteGOPOut',
    'StandIndivisible',
    'FlipThe8th',
    'waveCast',
    'WaveCastWA',
    'BuildTheBlueWave',
    '14yearsisenough',
    'flipthe3rd',
    'flipca25',
    'VoteBetoORourke4Texas',
    'ResistanceRises',
    'feelthebern',
]])
cons_hashtags = set([ht.lower() for ht in [
    'trumptrain',
    'maga',
    'walkaway',
    'qanon',
    'changethemedia',
    'greatawakening',
    'americafirst',
    'wwg1wga',
    'tcot',
    'kag',
    'patriotsunited',
    'qarmy',
    'ccot',
    'thegreatawakening',
    'q',
    'trump2020',
    'makeamericagreatagain',
    'liberalismisamentaldisorder',
    'trumpsarmy',
    'voteredtosaveamerica',
    'votered',
    'unitedvotered',
    'supportice',
    'keepredstatesred',
    'turnbluestatesred',
    'voteredtosavecalifornia',
    'MadMaxine',
    'VoteRedToSaveAmerica2018',
    'ResistTheResistance',
    'VoteAntonioToSaveCalifornia',
    'VoteRed2018',
    'GetMaxineOut',
    'RedWave2018',
    'blexit',
    'PledgeToVoteRed',
    'MAGA2020',
    'VoteRedSaveAmerica2018',
    'RedWave2018andBeyond',
    'redcalifornia',
    'VoteDemsOut',
    'MakeAmericsGreatAgain',
    'REDWAVECOMING',
    'RedTsunami',
    'VoteAntonioSabato',
    'VoteRedOrAmericaIsDead',
    'RedWave',
    'VoteRedSaveAmerica',
    'VoteRedMidterms2018',
    'CaravanInvasion',
    'WalkAwayFromDemocrats',
    'RedNovemeber',
    'RedNovember',
    'KeepFloridaRed',
    'BuildTheWall',
    'DemocratsHateAmerica',
    'VoteAntonio2018',
    'IVotedRED',
    'DefundPlannedParenthood',
    'MSM',
    'VoteRedToSaveCalifornia',
    'LyingLiberals',
    'UnhingedLeft',
    'CHOOSECRUZ',
    'RedTsunamiNov6',
    'whitepower',
    'prolife',
    'TeamDino',
    'waelex',
    'wapol',
    'betteroffnow',
    'votejaime',
    'wapol',
    'gregformontana',
    'teamgiantforte',
    'watergrab',
    'deandelivers',
    'AngryDemocratMob',
    'bluelivesmatter'
]])

def initialize_dict():
    # Create dictionary with candidate handles as keys and dictionary of counts of
    # liberal and conservative tweets in tweets that mention the candidate as values
    with open('candidate_handles.txt') as f:
        partisan_tweets_per_candidate = {}
        for line in f:
            partisan_tweets_per_candidate[line[1:-1].lower()] = {'liberal': {'total': 0, 'unique': 0}, 'conservative': {'total': 0, 'unique': 0}, 'neutral': {'total': 0, 'unique': 0}}
    return partisan_tweets_per_candidate

def initialize_posters_dict():
    posters = dict()
    with open('candidate_handles.txt') as f:
        for line in f:
            posters[line[1:-1].lower()] = set()
    return posters

def classify_tweet(tweet, lib_hashtags, cons_hashtags):
    lib_score = 0
    cons_score = 0
    tweet_sentiment = 'neutral'
    for hashtag in tweet['entities']['hashtags']:
        ht = hashtag['text'].lower()
        if ht in lib_hashtags or 'blue' in ht:
            lib_score +=1
        elif ht in cons_hashtags or 'red' in ht:
            cons_score += 1
    if lib_score > cons_score:
        tweet_sentiment = 'liberal'
    elif lib_score < cons_score:
        tweet_sentiment = 'conservative'
    return tweet_sentiment



with open('posters.pkl', 'wb') as posters_file:
    pickle.dump(initialize_posters_dict(), posters_file)
days = [
    '2018-10-22',
    '2018-10-23',
    '2018-10-24',
    '2018-10-25',
    '2018-10-26',
    '2018-10-27',
    '2018-10-28',
    '2018-10-29',
    '2018-10-30',
    '2018-10-31',
    '2018-11-01',
    '2018-11-02',
    '2018-11-03',
    '2018-11-04',
    '2018-11-05'
]
days.reverse()

for day in days:
    partisan_tweets_per_candidate = initialize_dict()
    # Keep track of tweets seen before
    tweet_ids = set()
    with open('posters.pkl', 'rb') as posters_file:
        posters = pickle.load(posters_file)
    files_for_day = []
    for file_name in os.listdir('.'):
        if day in file_name and 'all' not in file_name:
            files_for_day.append(file_name)
    for file_name in files_for_day:
        outfile_name = 'partisan_tweets_per_candidate_' + file_name[17:-5] + '.pkl'
        sys.stdout.write("parsing " + file_name + "...")
        sys.stdout.flush()

        with open(file_name) as infile, open(outfile_name, 'wb') as outfile:
            for line in infile:
                if line != None:
                    tweet = json.loads(line.rstrip('\n'))
                    try:
                        poster = tweet['user']['screen_name']
                        tweet_id = tweet['id_str']
                        if tweet_id not in tweet_ids:
                            tweet_ids.add(tweet_id)
                            # Classify tweet as liberal or conservative
                            tweet_sentiment = classify_tweet(tweet, lib_hashtags, cons_hashtags)

                            # Get the candidates mentioned in tweets
                            mentions = [mention_object['screen_name'].lower() for mention_object in tweet['entities']['user_mentions']]
                            # Update dictionary
                            for person in mentions:
                                try:
                                    partisan_tweets_per_candidate[person][tweet_sentiment]['total'] += 1
                                    if poster not in posters[person]:
                                        posters[person].add(poster)
                                        partisan_tweets_per_candidate[person][tweet_sentiment]['unique'] += 1
                                except:
                                    pass;
                    except:
                        pass;

            pickle.dump(partisan_tweets_per_candidate, outfile)
            print(partisan_tweets_per_candidate)
    with open('posters.pkl', 'wb') as posters_file, open('tweet_ids.pkl', 'wb') as tweet_ids_file:
        pickle.dump(posters, posters_file)
