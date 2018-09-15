import json
import os
import sys

class Parser:

    def __init__(self):
        pass

    def parse_json_file(self, infile):
        '''
        Parse a json file of scraped tweets.
        :param infile: The filename of the json file to be parsed
        :return: A list of dictionaries (each dictionary represents a parsed tweet).
        '''
        if (infile[-5:] != ".json"):
            print(infile + " is of invalid type.")
            return []

        data = []
        
        try:
            sys.stdout.write("parsing " + infile + "...")
            sys.stdout.flush()
            with open(infile) as f:
                for line in f:
                    if line != None:
                        data.append(json.loads(line.rstrip('\n')))
            print("done")
        except:
            print("FAILED")
            return []

        return data

    def parse_json_folder(self, infolder):
        '''
        Parse a folder filled with json files of scraped tweets.
        :param infile: The folder containing the json files to be parsed
        :return: A list of lists of dictionaries (each list represents a json file).
        '''
        all_data = {}
        for file in os.listdir(infolder):
            if (file[-5:] == ".json"):
                all_data[file] = self.parse_json_file(file)
        return all_data