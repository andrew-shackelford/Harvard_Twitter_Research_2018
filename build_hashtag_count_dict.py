import pickle, json, sys

def build_tweet_dict(from_file):
    '''
    NOTE: this code is no longer used in any of the other code in the file...

    Build a dictionary of tweet hashtags. The key to the dictionary is the individual hashtag, with the value being
    the number of instances of that hashtag. The file is assumed to be a json formatted file from the twitter stream
    :param from_file: a json-formatted file of tweets
    :return: a dictionary keyed by hashtag with value the count of tweets with that hashtag
    '''
    h_dict = {}
    for l in from_file:
        lj = json.loads(l)
        if ('entities' in lj) and ('hashtags' in lj['entities']):
            for h in lj['entities']['hashtags']:
                ht = h['text'].lower()
                print(ht)
                h_dict[ht] = h_dict.get(ht, 0) + 1
    return h_dict

def build_id_post_count(from_file):
    '''
    Build a dictionary keyed by tweeter id with value the number of tweets by that id in the file. The file passed in
    is assumed to be a json-formatted file of tweets scraped from the twitter stream
    :param from_file: a file in json format of tweets
    :return: a dictionary keyed by user id with value the number of tweets from that user
    '''
    id_dict = {}
    for l in from_file:
        lj = json.loads(l)
        if 'user' in lj :
            i = lj['user']['id']
            id_dict[i] = id_dict.get(i,0) + 1
    return id_dict

def build_count_dict(hash_dict):
    '''
    Take a dictionary keyed by some item with values counts of that item, and return a dictionary keyed by counts for
    the item with values the list of keys that have that value
    :param hash_dict: a dictionary of keys with values counts of those keys
    :return: a dictionary keyed by count with value a list of items with those counts
    '''
    count_d = {}
    for key, val in hash_dict.items():
        count_d[val] = count_d.get(val, [])
        count_d[val].append(key)
    return count_d

def build_tweet_id_dicts(from_file):
    '''
    Build two dictionaries from a json-formatted file of tweets. The first is a dictionary keyed by hashtag with values
    the number of occurrences of that hashtag. The second is a dictionary keyed by twitter user id with values the number
    of tweets by that user in the input file.
    :param from_file: a json formatted file of tweets scraped from the twitter feed
    :return: two dictionaries; one mapping hashtags to number of occurrences of the hashtag, the other mapping user ids
    to the number of tweets by that user
    '''
    h_dict = {}
    id_dict = {}
    for l in from_file:
        lj = json.loads(l)
        if ('entities' in lj) and ('hashtags' in lj['entities']):
            for h in lj['entities']['hashtags']:
                i = h['text'].lower()
                h_dict[i] = h_dict.get(i, 0) + 1
        if 'user' in lj:
            i = lj['user']['id']
            id_dict[i] = id_dict.get(i, 0) +1
    return h_dict, id_dict

def write_pickle(pickle_list):
    '''
    Taking a list of tuples of the form (file_name, object) write a pickle of that object to a newly created file with
    the name.
    :param pickle_list: A list of tuples of the form file_name, object
    :return: None
    '''
    for i in pickle_list:
        fout = open(i[0], 'wb')
        pickle.dump(i[1], fout)
        fout.close()
    return

def get_top_n(count_d, num):
    '''
    Print out the n most common values with their counts from a dictionary keyed by count with values a list of entities
    with those counts. If there are fewer than n entries in the dictionary, prints out the dictionary in descending order
    :param count_d: a dictionary keyed by count with values a list of entities with those counts
    :param num: The number of entities to print out
    :return: None
    '''
    scl = sorted(list(count_d.keys()), reverse = True)
    for i in range(0,num):
        if not i < len(scl):
            break
        c_i = scl[i]
        c_v = count_d[c_i]
        print(str(c_i) + ' : ' + str(c_v))
    return

def build_dicts(from_fname):
    '''
    From a json file of tweets, build a set of dictionaries:
        hashtag->number of occurrences of that tag
        number-of-occurrences->list of hashtag
        tweeter id -> number of tweets
        number of tweets -> list of tweeters
    Once these dictionaries have been built, save pickles of the dictionaries in files. This assumes the filename
    passed in has tha form 'tag_dataYYYY-MM-DD.json', and will create output files with corresponding dates
    :param from_fname: a file of tweets in json format, with a name of the form 'tag_dataYYYY-MM-DD.json'
    :return: None
    '''
    out_suffix = from_fname[8:-4] + 'pkl'
    fin = open(from_fname, 'r')
    h_dict, id_dict = build_tweet_id_dicts(fin)
    post_count_d = build_count_dict(h_dict)
    id_count_d = build_count_dict(id_dict)

    htd_name = 'hashtags2count_' + out_suffix
    htc_name = 'counts2hashtag_' + out_suffix
    id_name = 'id2count' + out_suffix
    idc_name = 'counts2id_' + out_suffix
    pickle_list = [(htd_name, h_dict), (htc_name, post_count_d), (id_name, id_dict), (idc_name, id_count_d)]

    write_pickle(pickle_list)
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python build_hashtag_count_dict.py infile.json')
        exit(1)
    
    print(sys.argv[1])
    build_dicts(sys.argv[1])
