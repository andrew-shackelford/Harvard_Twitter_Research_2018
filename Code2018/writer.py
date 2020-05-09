import pickle
import os
import sys

class Writer:

    def __init__(self):
        pass

    def write_to_pickle(self, data, outfile):
        '''
        Write an object out to a pickle file.
        :param data: The data to be written out to pickle.
        :param outfile: The desired filename of the pickle file to be written to.
        :return: None
        '''
        with open(outfile, 'wb') as f:
            try:
                sys.stdout.write("writing " + outfile + "...")
                sys.stdout.flush()
                pickle.dump(data, f)
                print("done")
            except:
                print("FAILED")