# October 12, 2018

### Analyzing tweet frequency by user

One thing that we have noticed over the course of our research is that there are many Twitter users that tweet extremely often, on the order of hundreds of tweets per day, and even 60+ tweets per hour. We would like to better visualize these users' behavior in order to determine the distinction between bots and legitimate users. To help solve this, I've written two helper classes, and two Python scripts that use those classes.  

##### Synthesizing Data

First, we need to synthesize the data in a convienent and compact manner. Using the `User_Analyzer` class, we can aggregate a collection of tweets into a dictionary keyed by `user_id`. This dictionary includes statistics such as number of tweets, and the date and time of each tweet by that user. This class supports reading both the initial `json` files and the intermediate `pkl` files, so it is not necessary to run `json` files through `json_to_pkl.py` before using this class. To use this class from the command line, run `python analyze_users.py`. This will perform the aggregation and write the result to a pickle file for user later.

##### Visualizing Data

Now, we need to visualize the data we've created. Using the `User_Visualizer` class, we can visualize the tweet frequency of certain users by hour. This class supports both visualizing specific `user_id`(s) or the top `x` users from a given data file. It will visualize the results using `matplotlib` and display a color-coded side-by-side bar graph. To use this class from the command line, run `python visualize_users.py`.