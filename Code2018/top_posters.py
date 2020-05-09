'''
A class that processes the id2count files in a DerivedFiles folder (in the same
directory) and

'''

import pickle
from collections import OrderedDict, defaultdict
import glob
import numpy as np
import matplotlib.pyplot as plt

class TopPosters:

    top50perday = []
    top50overall = {}

    def __init__(self):
        # load filenames of all files with 'id2count' in the name
        self.filenames = glob.glob('DerivedFiles/id2count*.pkl')

        # create list of dicts (one for each file)
        self.dictlist = []

        for file in self.filenames:
            with open(file, 'rb') as f:
                counts2id = pickle.load(f)
                self.dictlist.append(counts2id)

        # aggregate dicts
        ret = defaultdict(int)
        for d in self.dictlist:
            for k, v in d.items():
                ret[k] += v

        id2count_dict = dict(ret)

        self.ordered_counts = OrderedDict(sorted(id2count_dict.items(), key=lambda t: t[1], reverse=True))

    def topperday(self):
        for d in self.dictlist:
            ordered_count = OrderedDict(sorted(d.items(), key=lambda t: t[1], reverse=True))
            top50 = {k: ordered_count[k] for k in list(ordered_count)[:50]}
            self.top50perday.append(top50)
        print("Top 50 Per Day:", self.top50perday)


    def postcountover(self, count):
        # find user ids whose post counts are above a certain number
        #print("User IDs with a post count over %d", % count)
        for key, value in self.ordered_counts.items():
          if value > count:
            print(key, value)

    def topoverall(self):
        # find top 50 poster ids over all days
        self.top50overall = {k: self.ordered_counts[k] for k in list(self.ordered_counts)[:1000]}
        print("Top 50 Overall:", self.top50overall)

    def visualizetop50(self):
        # visualize distribution of top 50 over all time
        keys = []
        values = np.array([])

        for k, v in self.top50overall.items():
            keys.append(str(k))
            values = np.append(values, v)

        #plot
        fig, ax = plt.subplots()
        ax.hist(values, bins=25)
        ax.set_xlabel('counts')
        ax.set_ylabel('number of users')
        ax.set_title('Distribution of Top 50 Posters Overall')
        plt.show()

