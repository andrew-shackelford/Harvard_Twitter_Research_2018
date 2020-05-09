import argparse
import os
import parser
from Code2018 import writer


def main():
    argparser = argparse.ArgumentParser(description='Parse json files of tweets and export them to a pickle file.')
    argparser.add_argument("infile", help="The file or folders you wish to parse")
    argparser.add_argument("outfile", help="The destination pickle file")
    args = vars(argparser.parse_args())
    infile, outfile = args['infile'], args['outfile']

    json_parser = parser.Parser()

    if os.path.isdir(infile):
        data = json_parser.parse_json_folder(infile)
    elif os.path.isfile(infile):
        data = json_parser.parse_json_file(infile)
    else:
        print(infile + " is not a valid file.")
        return

    pickle_writer = writer.Writer()
    pickle_writer.write_to_pickle(data, outfile)

if __name__ == '__main__':
    main()