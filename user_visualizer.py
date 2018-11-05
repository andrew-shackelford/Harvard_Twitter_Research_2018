import os
import pickle
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

class User_Visualizer:

    def __init__(self, infile):
        if (infile[-4:] != ".pkl"):
            print(infile + " is of invalid type.")

        with open(infile) as f:
            self.file_name = infile
            self.users = pickle.load(f)

    def visualize_user_frequency(self, user_ids):
        '''
        Visualize the frequency of a users tweets from a pickle file of user tweet statistics.
        :param infile: The filename of the pickle file to be visualized
        :param user_ids: The user_ids to analyze
        :return: void
        '''        
        print("displaying graph of users in file " + self.file_name + "...")

        colors = cm.nipy_spectral(np.linspace(0, 1, len(user_ids)))

        width = 1./len(user_ids)

        graphs, titles = [], []

        fig = plt.figure(1, figsize=(14, 8))
        ax = fig.add_subplot(111)

        for idx, user_id in enumerate(user_ids):
            if user_id not in self.users:
                print("user_id not present")
            else:
                x, y = [], []
                sorted_keys = sorted(self.users[user_id]['tweet_times'].keys())
                for hour in sorted_keys:
                    count = self.users[user_id]['tweet_times'][hour]
                    x.append(hour + idx * width)
                    y.append(count)

                graphs.append(ax.bar(x, y, width, color=colors[idx], edgecolor="None"))
                titles.append(self.users[user_id]['screen_name'])
        
        fig.subplots_adjust(right=0.75)
        ax.legend(graphs, titles, bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        plt.show()

        print("done")

    def get_most_active_users(self, number=10):
        '''
        Print the most active users from a given pickle file of user tweet statistics.
        :param infile: The filename of the pickle file to be visualized
        :param number: The number of active users to print (default is 50)
        :return: void
        '''

        print("getting active users from " + self.file_name + "...")

        tuple_lst = []
        for user_id, user_stats in self.users.iteritems():
            tuple_lst.append((user_stats['count'], user_id))

        print("done")

        sorted_lst = sorted(tuple_lst, reverse=True)
        ret_lst = []

        for i in range(number):
            ret_lst.append(sorted_lst[i][1])

        return ret_lst



