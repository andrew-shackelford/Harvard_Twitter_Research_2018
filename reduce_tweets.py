import os, pickle, json, sys
import subprocess
import tweet_reduction_cl as tc

def get_file_list(file_pattern):
    ret_list = []
    all_files = os.listdir('.')
    for f in all_files:
        if file_pattern in f:
            ret_list.append(f)
    return ret_list

def file_prep(start_name):
    if start_name[-2:] == '.Z':
        subprocess.run(['uncompress', start_name])
        return start_name[:-2]
    elif start_name[-3:] == '.gz':
        subprocess.run(['gunzip', start_name])
        return start_name[:-3]
    else:
        return start_name

def file_compress(f_name):
    subprocess.run(['gzip', fname])
    return

def write_daily_pickles(fname, tweet_dict, retweet_dict):
    tweet_out = open(fname + 'tweets' + '.pkl', 'wb')
    pickle.dump(tweet_dict, tweet_out)
    tweet_out.close()

    retweet_out = open(fname + 'retweets' + '.pkl', 'wb')
    pickle.dump(retweet_dict, retweet_out)
    retweet_out.close()
    return


def extract_reduction(fname, tweet_ids, tweeter_dict):
    tweet_dict = {}
    retweet_dict = {}
    fin = open(fname, 'r')
    total_tweets = 0
    for l in fin:
        try:
            jl = json.loads(l)
        except:
            continue

        if 'id_str' in jl:
            total_tweets += 1
            if jl['id_str'] not in tweet_ids:
                tweet_dict[jl['id_str']] = tc.tweet_tags(jl)
                tweet_ids.add(jl['id_str'])
            if jl['user']['id_str'] not in twit_ids:
                tweeter_dict[jl['user']['id_str']] = tc.tweeter(jl)
            else:
                tweeter_dict[jl['user']['id_str']].incr_tweet_count()

            if jl['text'][:4] == "RT @":  # gather retweets only
                source_handle = jl['text'].split(":")[0][4:]
                retweet_handle = jl['user']['screen_name']
                if source_handle not in retweet_dict:
                    retweet_dict[source_handle] = set()
                retweet_dict[source_handle].add(retweet_handle)

    fin.close()
    write_daily_pickles(fname, tweet_dict, retweet_dict)
    return total_tweets


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python reduce_tweets.py filePattern')
        sys.exit()

    f_list = get_file_list(sys.argv[1])

    tweet_ids = set()
    twit_ids = {}
    tweet_count = 0

    for f in f_list:
        if '.json' not in f:
            continue
        print (f)
        fname = file_prep(f)
        t_count = extract_reduction(fname, tweet_ids, twit_ids)
        tweet_count += t_count
        print('about to zip file')
        file_compress(f)

    tweet_out = open('all_tweet_set.pkl', 'wb')
    pickle.dump(tweet_ids, tweet_out)
    tweet_out.close()

    print ('total number of tweets = ' + str(tweet_count))
    print ('length of the tweet set = ' + str(len(tweet_ids)))
    print ('total number of tweeters = ' + str(len(twit_ids)))



