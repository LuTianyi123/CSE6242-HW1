
import csv
import json
import time
import tweepy

# Use Python 3.5
# You must use Python 3.0 or above
# For those who have been using python 2.7.x before, here is an article explaining key differences between python 2.7x & 3.x
# http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put in your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>

    with open(key_file) as data_file:
        data = json.load(data_file)

    return data["api_key"], data["api_secret"], data["token"], data["token_secret"]

# Q1.b - 5 Marks
def getFollowers(api, root_user, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers of 'root_user'
    # rtype: list containing entries in the form of a tuple (follower, root_user)

    primary_followers = []
    for user in tweepy.Cursor(api.followers, screen_name=root_user).items():
        primary_followers.append((user.screen_name, root_user))
        if len(primary_followers) == no_of_followers:
            break

    return primary_followers

# Q1.b - 7 Marks
def getSecondaryFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])

    secondary_followers = []
    for u in followers_list:
        primary_user = u[0]
        list = []
        for user in tweepy.Cursor(api.followers, screen_name=primary_user, count=no_of_followers).items():
            list.append((user.screen_name, primary_user))
            if len(list) == no_of_followers:
                break
        secondary_followers.extend(list)

    return secondary_followers

# Q1.c - 5 Marks
def getFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    primary_friends = []
    for user in tweepy.Cursor(api.friends, screen_name=root_user, count=no_of_friends).items():
        primary_friends.append((root_user, user.screen_name))
        if len(primary_friends) == no_of_friends:
            break

    return primary_friends

# Q1.c - 7 Marks
def getSecondaryFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    secondary_friends = []
    for u in friends_list:
        primary_friend = u[1]
        list = []
        for user in tweepy.Cursor(api.friends, screen_name=primary_friend, count=no_of_friends).items():
            list.append((primary_friend, user.screen_name))
            if len(list) == no_of_friends:
                break
        secondary_friends.extend(list)

    return secondary_friends

# Q1.b, Q1.c - 6 Marks
def writeToFile(data, output_file):
    # write data to output file
    # rtype: None
    with open(output_file, 'w') as csvfile:
        fieldnames = ['source', 'target']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for item in data:
            writer.writerow({'source': item[0], 'target': item[1]})


"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_FOLLOWERS = 'followers.csv'
    OUTPUT_FILE_FRIENDS = 'friends.csv'

    ROOT_USER = 'PoloChau'
    NO_OF_FOLLOWERS = 10
    NO_OF_FRIENDS = 10


    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)
    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
    secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)

    followers = primary_followers + secondary_followers
    primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)

    secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)

    friends = primary_friends + secondary_friends
    writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
    writeToFile(friends, OUTPUT_FILE_FRIENDS)

if __name__ == '__main__':
    testSubmission()





