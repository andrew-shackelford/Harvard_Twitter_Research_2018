import os, pickle

def build_dict(l_in):
    '''
    From a list of (hashtag, count) pairs, build a dictionary keyed by the lower-case version of the hashtag with
    value the sum of the counts of the cased variations of the hashtag
    :param l_in: a list of (hashtag, count) pairs. 
    :return: a dictionary keyed by hashtag.lower() with value the sum of all cased-hashtags that reduce to the key
    '''
    ret_dict = {}
    for l in l_in:
        k = l[0].lower()
        if k in ret_dict:
            ret_dict[k] += l[1]
        else:
            ret_dict[k] = l[1]
    return ret_dict

if __name__ == '__main__':
    dir_l = os.listdir('.')
    for fname in dir_l:
        print(fname)
        in_f = open(fname, 'r')
        in_l = pickle.load(in_f)
        out_d = build_dict(in_l)
        out_fname = '_d'.join([fname[:-4], '.pkl'])
        out_f = open(out_fname, 'w')
        pickle.dump(out_d, out_f)
        in_f.close()
        out_f.close()