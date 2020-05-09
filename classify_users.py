import argparse
import user_classifier
import os


def main():
    argparser = argparse.ArgumentParser(description='Manually classify whether users are bots or not.')
    argparser.add_argument("infile", help="The file you wish to classify. Results will also be written to this file.")
    argparser.add_argument("--num_tweets", help="The minimum number of tweets a user must have in order to be classified (default is 10).", type=int, default=10)
    args = vars(argparser.parse_args())
    infile = args['infile']
    num_tweets = args['num_tweets']

    classifier = user_classifier.User_Classifier()

    if os.path.isfile(infile):
        data = classifier.classify_users(infile, num_tweets)
    else:
        print(infile + " is not a valid file.")
        return
        
if __name__ == '__main__':
    main()