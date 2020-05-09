import argparse
import user_visualizer
import os


def main():
    argparser = argparse.ArgumentParser(description='Visualize pickle files of tweets statistics.')
    argparser.add_argument("infile", help="The file you wish to visualize")
    argparser.add_argument("--user_id", help="The user_id of a user you wish to visualize (this argument may be repeated)", type=int, action='append', default=[])
    argparser.add_argument("--number", help="The number of top tweeting users you wish to visualize if no user_ids are provided (default is 10)", type=int, default=10)
    args = vars(argparser.parse_args())
    infile = args['infile']

    if os.path.isfile(infile):
        print("loading " + infile + "...")
        visualizer = user_visualizer.User_Visualizer(infile)
        print("done")
        
        if len(args['user_id']) > 0:
            data = visualizer.visualize_user_frequency(args['user_id'])
        else:
            user_ids = visualizer.get_most_active_users(args['number'])
            visualizer.visualize_user_frequency(user_ids)
    else:
        print(infile + " is not a valid file.")
        return

if __name__ == '__main__':
    main()