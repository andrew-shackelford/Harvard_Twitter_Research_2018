import os, pickle, json, sys, csv
import subprocess
from Code2018 import tweet_reduction_cl as tc


def get_file_list(file_pattern):
    """
    Return a list of files that contain the string specified in the argument. This works for the current directory
    only.
    :param file_pattern: a string that will be matched to add files to the list
    :return: a list of files in the current directory that contain the string file_pattern
    """
    ret_list = []
    all_files = os.listdir('..')
    for f in all_files:
        if file_pattern in f:
            ret_list.append(f)
    return ret_list

def file_prep(start_name):
    """
    Uncompress a file if needed. Will handle both compressed and gzipped files. If the file is neither compressed (determined
    by having a .Z extension) or gzipped (determined by having a .gz extenstion) return the name of the file and do
    nothing
    :param start_name: name of the file to be uncompressed or unzipped
    :return: The name of the uncompressed file, or the name of the original file if it was neither compressed nor
    gzipped.
    """
    if start_name[-2:] == '.Z':
        print ('Uncompressing ', start_name)
        subprocess.run(['uncompress', start_name])
        return start_name[:-2]
    elif start_name[-3:] == '.gz':
        print ('Unzipping', start_name)
        subprocess.run(['gunzip', start_name])
        return start_name[:-3]
    else:
        return start_name

def file_compress(f_name):
    """
    Gzip a file; this is run when the extraction is done to save space.
    :param f_name: Name of the file to gzip
    :return: None
    """
    print ('Running gzip on', fname)
    subprocess.run(['gzip', fname])
    return

def write_daily_pickles(fname, retweet_dict):
    """
    Write a pickle file for the daily retweets extracted from a file, using the name of the file with the extension
    removed and 'retweets.pkl' added to the name
    :param fname: The name of the file from which the retweets have been extracted
    :param retweet_dict: The dictionary of retweets
    :return: None
    """
    retweet_out = open(fname[:-4] + 'retweets.pkl', 'wb')
    pickle.dump(retweet_dict, retweet_out)
    retweet_out.close()
    return


def extract_reduction(fname, tweet_ids, tweeter_dict):
    """
    Extracts s subset of the information that is in the collection of tweets for the named file. Skipping any tweets it
    has seen before, it creates a tweet_tag object and then writes that object out to a .csv file. While doing this, it
    also creates a dictionary of all those who tweet, creating tweeter objects and holding those in a
    dictionary that will be pickled on a per-day basis. A set of tweeters is also kept.
    :param fname: Name of the .json file containing the tweets to be extracted and reduced
    :param tweet_ids: A set of tweet ids, to insure de-duplicaiton
    :param tweeter_dict: A dictionary of all tweeters
    :return: The number of tweets encountered in the file. The function will also create a .csv file based on
    the input name, and a pickle file based on the input name. The .csv will contain the reduced tweets, while
    the .pkl file will contain the retweet dictionary.
    """
    retweet_dict = {}
    fin = open(fname, 'r')
    fout = open(fname[:-4] + 'tweets' + '.csv', 'w')
    csv_tweet_out = csv.writer(fout)
    total_tweets = 0
    for l in fin:
        try:
            jl = json.loads(l)
        except:
            continue

        if 'id_str' in jl:
            total_tweets += 1
            if jl['id_str'] not in tweet_ids:
                csv_tweet_out.writerow(tc.tweet_tags(jl).get_values_as_list())
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
    fout.close()
    write_daily_pickles(fname, retweet_dict)
    return total_tweets


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python reduce_tweets.py filePattern')
        sys.exit()

    base_name = sys.argv[1]
    f_list = get_file_list(base_name)

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

    tweet_out = open(base_name +'_all_tweet_set.pkl', 'wb')
    pickle.dump(tweet_ids, tweet_out)
    tweet_out.close()

    twit_out = open(base_name + '_all_tweeters.csv', 'w')
    twit_c = csv.writer(twit_out)
    for v in twit_ids.values():
        twit_c.writerow(v.get_values_as_list())
    twit_out.close()

    print ('Statistics for files matching', base_name)
    print ('total number of tweets = ' + str(tweet_count))
    print ('length of the tweet set = ' + str(len(tweet_ids)))
    print ('total number of tweeters = ' + str(len(twit_ids)))



