import json
import os
import sys

senate_incumbent_handle_mention_count = {
                                        "@SenShelby" : 0,
                                        "@SenatorSessions" : 0,
                                        "@SenDanSullivan" : 0,
                                        "@lisamurkowski" : 0,
                                        "@SenJohnMcCain" : 0,
                                        "@JeffFlake" : 0,
                                        "@SenTomCotton" : 0,
                                        "@JohnBoozman" : 0,
                                        "@SenFeinstein" : 0,
                                        "@KamalaHarris" : 0,
                                        "@SenCoryGardner" : 0,
                                        "@SenBennetCO" : 0,
                                        "@ChrisMurphyCT" : 0,
                                        "@SenBlumenthal" : 0,
                                        "@SenCoonsOffice" : 0,
                                        "@SenatorCarper" : 0,
                                        "@marcorubio" : 0,
                                        "@sendavidperdue" : 0,
                                        "@SenatorIsakson" : 0,
                                        "@SenBrianSchatz" : 0,
                                        "@maziehirono" : 0,
                                        "@SenatorRisch" : 0,
                                        "@MikeCrapo" : 0,
                                        "@RepDuckworth" : 0,
                                        "@SenatorDurbin" : 0,
                                        "@SenDonnelly" : 0,
                                        "@ToddYounIN" : 0,
                                        "@ChuckGrassley" : 0,
                                        "@SenJoniErnst" : 0,
                                        "@SenPatRoberts" : 0,
                                        "@JerryMoran" : 0,
                                        "@RandPaul" : 0,
                                        "@McConnellPress" : 0,
                                        "@JohnKennedyLA" : 0,
                                        "@BillCassidy" : 0,
                                        "@SenAngusKing" : 0,
                                        "@SenatorCollins" : 0,
                                        "@ChrisVanHollen" : 0,
                                        "@SenatorCardin" : 0,
                                        "@SenWarren" : 0,
                                        "@SenMarkey" : 0,
                                        "@SenStabenow" : 0,
                                        "@SenGaryPeters" : 0,
                                        "@amyklobuchar" : 0,
                                        "@alfranken" : 0,
                                        "@SenatorWicker" : 0,
                                        "@SenThadCochran" : 0,
                                        "@McCaskillOffice" : 0,
                                        "@RoyBlunt" : 0,
                                        "@SenatorTester" : 0,
                                        "@SteveDaines" : 0,
                                        "@SenSasse" : 0,
                                        "@SenatorFischer" : 0,
                                        "@SenDeanHeller" : 0,
                                        "@CatherineForNV" : 0,
                                        "@SenatorShaheen" : 0,
                                        "@Maggie_Hassan" : 0,
                                        "@SenatorMenendez" : 0,
                                        "@CoryBooker" : 0,
                                        "@SenatorTomUdall" : 0,
                                        "@MartinHeinrich" : 0,
                                        "@SenSchumer" : 0,
                                        "@SenGillibrand" : 0,
                                        "@SenThomTillis" : 0,
                                        "@SenatorBurr" : 0,
                                        "@SenJohnHoeven" : 0,
                                        "@SenatorHeitkamp" : 0,
                                        "@senrobportman" : 0,
                                        "@SenSherrodBrown" : 0,
                                        "@SenatorLankford" : 0,
                                        "@InhofePress" : 0,
                                        "@RonWyden" : 0,
                                        "@SenJeffMerkley" : 0,
                                        "@SenToomey" : 0,
                                        "@SenBobCasey" : 0,
                                        "@SenWhitehouse" : 0,
                                        "@SenJackReed" : 0,
                                        "@SenatorTimScott" : 0,
                                        "@GrahamBlog" : 0,
                                        "@SenJohnThune" : 0,
                                        "@SenatorRounds" : 0,
                                        "@SenBobCorker" : 0,
                                        "@SenAlexander" : 0,
                                        "@SenTedCruz" : 0,
                                        "@JohnCornyn" : 0,
                                        "@SenMikeLee" : 0,
                                        "@SenOrrinHatch" : 0,
                                        "@SenSanders" : 0,
                                        "@SenatorLeahy" : 0,
                                        "@MarkWarner" : 0,
                                        "@timkaine" : 0,
                                        "@PattyMurray" : 0,
                                        "@SenMikeLee" : 0,
                                        "@Sen_JoeManchin" : 0,
                                        "@SenCapito" : 0,
                                        "@SenRonJohnson" : 0,
                                        "@SenatorBaldwin" : 0,
                                        "@SenatorEnzi" : 0,
                                        "@SenJohnBarrasso" : 0
}

def parse_json_file(infile):
    '''
    Parse a json file of scraped tweets.
    :param infile: The filename of the json file to be parsed
    :return: A list of dictionaries (each dictionary represents a parsed tweet).
    '''
    if (infile[-5:] != ".json"):
        print(infile + " is of invalid type.")
        return []

    data = []
    can_dict = {"@TheDemocrats" : 0, "@GOP": 0}

    try:
        sys.stdout.write("parsing " + infile + "...")
        sys.stdout.flush()
        printvar = True
        with open(infile) as f:
            # Parse line which will be a parsed tweet
            # For each tweet, look at the text field and scrape the mentions
            for line in f:
                if line != None:
                    tweet = json.loads(line.rstrip('\n'))
                    text = tweet['text']

                    if printvar:
                        print("inside")
                        printvar = False

                    while text.find('@') > -1:
                        # Find a mention by searching for @ symbol then cutting text to the length of that mention
                        start_i = text.find('@')
                        # Current delimiters: space, end of string,
                        # Might need other delimiters for mention, possibly '\n', '.', ':'
                        length_index = len(text[start_i:]) - 1
                        space_index = text[start_i:].find(' ')
                        colon_index = text[start_i:].find(':')
                        comma_index = text[start_i:].find(',')
                        period_index = text[start_i:].find('.')
                        #dots_index = text[start_i:].find('...')
                        indeces = [length_index, space_index, colon_index, comma_index, period_index]

                        indeces = list(filter(lambda x: x > 0, indeces))

                        end_i = min(indeces)

                        mention = text[start_i: start_i + end_i]
                        # Now that we have a mention, increment counter
                        #print(mention)
                        if mention in can_dict:
                            can_dict[mention] += 1
                        if mention in senate_incumbent_handle_mention_count:
                            senate_incumbent_handle_mention_count[mention] += 1

                        # Here's our bug, text is not updating correctly
                        if start_i + end_i == len(text) - 1:
                            text = ""
                        else:
                            text = text[start_i + end_i:]

                        # if text.find('@') == -1:
                        #     break

        print("done")
    except:
        print("FAILED")
        return []

    #return can_dict
    return senate_incumbent_handle_mention_count

parse_json_file('candidate_handles1A2018-10-27.json')
parse_json_file('candidate_handles1B2018-10-27.json')
parse_json_file('candidate_handles2A2018-10-27.json')
parse_json_file('candidate_handles2B2018-10-27.json')
parse_json_file('candidate_handles3A2018-10-27.json')
parse_json_file('candidate_handles3B2018-10-27.json')
#print(senate_incumbent_handle_mention_count)
new_dict = sorted(senate_incumbent_handle_mention_count.items(), key=lambda kv: kv[1])
print(new_dict)

blue_senate = { "@SenFeinstein",
                "@KamalaHarris",
                "@SenBennetCO",
                "@ChrisMurphyCT",
                "@SenBlumenthal",
                "@SenCoonsOffice",
                "@SenatorCarper",
                "@SenBrianSchatz",
                "@maziehirono",
                "@RepDuckworth",
                "@SenatorDurbin",
                "@SenDonnelly",
                "@SenAngusKing",
                "@ChrisVanHollen",
                "@SenatorCardin",
                "@SenWarren",
                "@SenMarkey",
                "@SenStabenow",
                "@SenGaryPeters",
                "@amyklobuchar",
                "@alfranken",
                "@McCaskillOffice",
                "@SenatorTester",
                "@CatherineForNV",
                "@SenatorShaheen",
                "@Maggie_Hassan",
                "@SenatorMenendez",
                "@CoryBooker",
                "@SenatorTomUdall",
                "@MartinHeinrich",
                "@SenSchumer",
                "@SenGillibrand",
                "@SenatorHeitkamp",
                "@SenSherrodBrown",
                "@RonWyden",
                "@SenJeffMerkley",
                "@SenBobCasey",
                "@SenWhitehouse",
                "@SenJackReed",
                "@SenAlexander",
                "@SenSanders",
                "@SenatorLeahy",
                "@MarkWarner",
                "@timkaine",
                "@PattyMurray",
                "@Sen_JoeManchin",
                "@SenatorBaldwin", }

blue_total = 0
red_total = 0
for candidate in senate_incumbent_handle_mention_count.keys():
    if candidate in blue_senate:
        blue_total += senate_incumbent_handle_mention_count[candidate]
        print(senate_incumbent_handle_mention_count[candidate], "mentions of", candidate)
    else:
        red_total += senate_incumbent_handle_mention_count[candidate]

print(blue_total, "liberal mentions")
print(red_total, "conservative mentions")
