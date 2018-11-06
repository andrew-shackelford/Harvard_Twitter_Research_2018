import pickle

dates = [
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
segments = [
    '1A',
    '1B',
    '2A',
    '2B',
    '3A',
    '3B'
]
# We fucked up and need to find the last file dumped each date so...
for date in dates:
    # Make dictionary where keys are date-segments and values are the sum of tweets
    dict_of_checksums = {}
    for segment in segments:
        checksum = 0
        partisan_tweets_per_candidate = pickle.load(open('data/partisan_tweets_per_candidate_' + segment + date + '.pkl', 'rb'))
        for handle in partisan_tweets_per_candidate.keys():
            for sentiment in partisan_tweets_per_candidate[handle].keys():
                for type in partisan_tweets_per_candidate[handle][sentiment]:
                    checksum += partisan_tweets_per_candidate[handle][sentiment][type]
        dict_of_checksums[segment + date] = checksum
    real_segment_date = max(dict_of_checksums, key=dict_of_checksums.get)

    # Make copy of the correct dictionary to use for analysis
    with open('data/partisan_tweets_per_candidate_' + real_segment_date + '.pkl', 'rb') as infile, \
        open('data/partisan_tweets_per_candidate_' + date + '.pkl', 'wb') as outfile:
        dict = pickle.load(infile)
        pickle.dump(dict, outfile)
