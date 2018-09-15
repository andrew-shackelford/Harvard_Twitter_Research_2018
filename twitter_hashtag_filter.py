import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import os, sys
from datetime import date

def load_dict(auth_d, l):
    '''
    Load the contents of a line into a dictionary, using the first word of the
    line as the key and the rest of the line as the value.
    :param auth_d: The dictionary to be populated
    :param l: The line that contains the key and the value, both as strings
    :return: None
    '''
    s = l.find(' ')
    k = l[ :s]
    v = l[s+1:]
    auth_d[k] = v

def read_config_file(file_name):
    '''
    Read a set of configuration parameters from a text file, and return a dictionary with those parameters.

    This assumes that the configuration file has each configuration parameter on a line, with the name of the parameter
    as the first word of the line, followed by a single space, followed by the value of the parameter. All names and
    parameters are assumed to be strings.

    The function will read each line, and place the name/parameter pair into a dictionary keyed by the name with value
    the parameter. Conversion of the parameters to something other than string should be done when the parameter is used.

    :param file_name: Name of the file containing the configuration
    :return: a dictionary with key the name of the configuration parameter and value the configuration value
    '''
    config_dict = {}
    fin = open(file_name, 'r')

    for line in fin:
        if line == '\n':
            pass
        elif line[0] == '#':
            pass
        else:
            load_dict(config_dict, line[:-1])

    fin.close()
    return config_dict

def make_auth(auth_dict):
    '''
    Create a tweepy auth object. This will use the contents of the dictionary that has been handed in that contains the
    access token and consumer keys. The assumption is that the dictionary contains the authorization tokens needed
    :param auth_dict: dictionary containing the authentication information
    :return: A tweepy auth object
    '''
    auth = OAuthHandler(auth_dict['consumer_key'], auth_dict['consumer_secret'])
    auth.set_access_token(auth_dict['access_token'], auth_dict['access_secret'])
    return auth


class MyListener(StreamListener):

    def __init__(self, out_directory, out_fname):
        self.count = 1
        self.directory = out_directory
        self.fname = out_fname
        self.date = date.today()
        self.outname = os.path.sep.join([out_directory, out_fname])
        self.outname = self.outname + str(self.date) + '.json'
        try:
            self.outfile = open(self.outname, 'a')
        except BaseException as e:
            print(self.outname)
            print('error on file open'+ str(e))
            exit(1)

    def on_data(self, t_data):
        try:
            self.outfile.write(t_data)
            if self.count < 100:
                self.count += 1
            else:
                self.count = 1
                if self.check_new_date():
                    self.use_file()
            return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

    def use_file(self):
        self.outfile.close()
        if self.date != date.today():
            self.date = date.today()
        self.outname = os.path.sep.join([self.directory, self.fname])
        self.outname = self.outname + str(self.date) + '.json'
        try:
            self.outfile = open(self.outname, 'a')
        except BaseException as e:
            print('error opening new file')
            exit(1)

    def check_new_date(self):
        if self.date != date.today():
            return True
        else:
            return False

def get_filter_list(config_d):
    '''
    Creates a string of comma-separated entries from a file. If there is no hashtag_file entry in
    the configuration file, returns the empty string.
    :param config_d: A
    :return:
    '''
    ret_data = ''
    if 'filter_file' in config_d:
        for line in open(config_d['filter_file'], 'r'):
            if line != '\n':
                ret_data += ',' + line[:-1]
    return ret_data

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: python twitter_hashtag_filter.py config_file_name')
        sys.exit(1)

    fname = sys.argv[1]
    config = read_config_file(fname)

    auth = make_auth(config)
    api = tweepy.API(auth)

    data = get_filter_list(config)

    if 'output_directory' in config:
        out_dir = config['output_directory']
    else:
        out_dir = '.'
    if 'output_file' in config:
        out_file = config['output_file']
    else:
        out_file = 'test_output'

    if data == '':
        print('No terms specified for tracking, program exiting')
        sys.exit(1)

    while True:
        try:
            twitter_stream = Stream(auth, MyListener(out_dir, out_file))
            twitter_stream.filter(track=[data])
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            pass
