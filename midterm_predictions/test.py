
import pickle
dict = pickle.load(open('partisan_tweets_per_candidate_1A2018-11-02.pkl', 'rb'))
for key in dict.keys():
    for type in dict[key].keys():
        if dict[key][type]['unique'] == 0 and dict[key][type]['total'] != 0:
            print(dict[key])
