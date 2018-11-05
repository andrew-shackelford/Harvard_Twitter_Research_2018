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

dir = os.listdir('data')

for file_name in dir:
    outfile_name = 'partisan_tweets_per_candidate_' + file_name[17:-5] + '.pkl'
    sys.stdout.write("parsing " + file_name + "...")
    sys.stdout.flush()
    # Create dictionary with candidate handles as keys and dictionary of counts of
    # liberal and conservative tweets in tweets that mention the candidate as values
    with open('candidate_handles' + file_name[17:19] + '.txt') as f:
        partisan_tweets_per_candidate = {}
        handles = []
        for line in f:
            partisan_tweets_per_candidate[line[:-1].lower()] = {'liberal': {'total': 0, 'unique': 0}, 'conservative': {'total': 0, 'unique': 0}, 'neutral': {'total': 0, 'unique': 0}}
            handles.append(line[:-1].lower())

    with open('data/' + file_name) as infile, open(outfile_name, 'wb') as outfile:
        # Keep track of posters
        posters = set()
        for line in infile:
            if line != None:
                tweet = json.loads(line.rstrip('\n'))
                try:
                    poster = tweet['user']['screen_name']

                    # Classify tweet as liberal or conservative
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

                    # Get the candidates mentioned in tweets
                    # mentions = re.findall('@[a-zA-Z0-9_]{1,15}', tweet['text'].lower())
                    mentions = [mention_object['screen_name'] for mention_object in tweet['entities']['user_mentions']]
                    # Update dictionary
                    for person in mentions:
                        if person in handles:
                            try:
                                partisan_tweets_per_candidate[person][tweet_sentiment]['total'] += 1
                                if poster not in posters:
                                    partisan_tweets_per_candidate[person][tweet_sentiment]['unique'] += 1
                                    posters.append(poster)
                            except:
                                pass;
                except:
                    pass;
        pickle.dump(partisan_tweets_per_candidate, outfile)
        print(partisan_tweets_per_candidate)
