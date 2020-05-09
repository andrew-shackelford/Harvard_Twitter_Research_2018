import os, pickle, json, sys
import subprocess
import thinned_tweet_obj as tt


def get_file_list(file_pattern):
    """
    Return a list of files that contain the string specified in the argument. This works for the current directory
    only.
    :param file_pattern: a string that will be matched to add files to the list
    :return: a list of files in the current directory that contain the string file_pattern
    """
    ret_list = []
    all_files = os.listdir('.')
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

def file_compress(fname):
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
    retweet_out = open(fname[:-4] + '_thin.pkl', 'wb')
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
    thin_l = []
    dup_count = 0
    fin = open(fname, 'r')
    t_l = json.load(fin)
    fin.close()
    for l in t_l:
        if 'id_str' in l and l['id_str'] not in tweet_ids:
            thin_l.append(tt.tweet(l))
            tweet_ids.add(l['id_str'])
            tweeter_dict[l['id_str']] = tweeter_dict.setdefault(l['id_str'], 0) + 1
    print("Duplicate count = " + str(dup_count))
    return thin_l


def reduce_files(write_dir):
    f_list = get_file_list('.json')

    tweet_ids = set()
    twit_ids = {}

    for f in f_list:
        if '.json' not in f:
            continue
        print (f)
        fname = file_prep(f)
        thin_list = extract_reduction(fname, tweet_ids, twit_ids)
        print('about to zip file')
        file_compress(fname)
        out_fname = write_dir + '/'+ fname
        write_daily_pickles(out_fname, thin_list)


    twit_out = open(write_dir + '/all_tweeters.pkl', 'wb')
    pickle.dump(twit_ids, twit_out)
    twit_out.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python reduce_tweets.py directory_pattern')
        sys.exit()

    base_dir_name = sys.argv[1]
    dir_list = os.listdir('.')
    for d in dir_list:
        if base_dir_name in d and 'reduced' not in d:
            target_dir = d + 'reduced'
            os.makedirs(target_dir)
            out_dir = '/'.join(['..', target_dir])
            os.chdir(d)
            reduce_files(out_dir)
            os.chdir('..')



