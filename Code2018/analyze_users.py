import argparse
import user_analyzer
import os
from Code2018 import writer


def main():
    argparser = argparse.ArgumentParser(description='Analyze pickle or json files of tweets and determine how often and when a user tweets.')
    argparser.add_argument("infile", help="The file or folder you wish to analyze")
    argparser.add_argument("outfile", help="The destination pickle file")
    args = vars(argparser.parse_args())
    infile, outfile = args['infile'], args['outfile']

    analyzer = user_analyzer.User_Analyzer()

    if os.path.isdir(infile):
        data = analyzer.analyze_user_folder(infile)
    elif os.path.isfile(infile):
        data = analyzer.analyze_user_file(infile)
    else:
        print(infile + " is not a valid file.")
        return

    if data == []:
        return
        
    pickle_writer = writer.Writer()
    pickle_writer.write_to_pickle(data, outfile)

if __name__ == '__main__':
    main()