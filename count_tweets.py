import argparse
import tweet_counter
import os
import writer
import pickle

def main():
    argparser = argparse.ArgumentParser(description='Count the number of tweets per user from the reduced tweet files.')
    argparser.add_argument("infile", help="The file or folder you wish to count")
    argparser.add_argument("outfile", help="The destination pickle file")
    argparser.add_argument("--count_file", help="A (optional) pickle file of counts that you wish to append to.", type=str, default="")
    
    args = vars(argparser.parse_args())
    infile, outfile, count_file = args['infile'], args['outfile'], args['count_file']
    
    counter = tweet_counter.Tweet_Counter()

    if os.path.isfile(count_file):
        with open(count_file, 'rb') as data_file:
            data = pickle.load(data_file)
    else:
        data = {}

    if os.path.isdir(infile):
        data = counter.count_tweets_folder(infile, data)
    elif os.path.isfile(infile):
        data = counter.count_tweets_file(infile, data)
    else:
        print(infile + " is not a valid file or folder.")
        return

    if data == {}:
        return
        
    pickle_writer = writer.Writer()
    pickle_writer.write_to_pickle(data, outfile)

if __name__ == '__main__':
    main()