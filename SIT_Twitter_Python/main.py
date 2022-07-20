import tweepy
from math import log

import config
import draw

client = tweepy.Client(config.bearer_token)  # start client with bearer token


# collect data----------------------------------------------------------------------------------------------------------


# get member ids from twitter list
def get_list_members(list_id):
    members_list = []
    members = client.get_list_members(list_id)  # get list of users from id

    for w in range(len(members.data)):
        members_list.append(members.data[w]['id'])  # store user id from data to members_list

    return members_list


class TwitterUser:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user = client.get_user(id=self.user_id, user_fields='public_metrics')  # get user info
        self.user_metrics = self.user.data.public_metrics  # filter info to get public metrics
        self.user_timeline = client.get_users_tweets(self.user_id, max_results=50, tweet_fields='public_metrics')[0]
        # get tweets from user id, filter everything except 'data'

    def follower_count(self):
        return self.user_metrics['followers_count']  # get followers count from user metrics

    def mnrt(self):
        retweets = []

        if self.user_timeline is not None:
            for i in range(len(self.user_timeline)):
                retweets.append(self.user_timeline[i].data['public_metrics']['retweet_count'])
                # get retweet_count from tweet metrics and store in retweets list
        else:
            retweets.append(0)

        return sum(retweets) / len(retweets)  # mean retweet number of last tweets from user


# main------------------------------------------------------------------------------------------------------------------


def main():
    x = []  # x axis, list of followers
    y = []  # y axis, list of mnrt
    log_x = []  # log values of followers
    log_y = []  # log values of mnrt

    user_list = get_list_members(config.twitter_list)

    for z in range(len(user_list)):
        user = TwitterUser(user_id=user_list[z])  # cycle every user in list
        user_fc = user.follower_count()
        user_mnrt = user.mnrt()

        # store follower count and mnrt to use in diagrams
        x.append(user_fc)
        y.append(user_mnrt)

        # store log values of followers and mnrt to use in diagrams
        if user_mnrt > 0:
            log_y.append(log(user_mnrt))  # get log value of mnrt if mnrt > 0
        else:
            log_y.append(user_mnrt)
        if user_fc > 0:
            log_x.append(log(user_fc))  # get log value of followers if followers > 0
        else:
            log_x.append(user_fc)

    draw.diagrams(x, y, log_x, log_y)


if __name__ == '__main__':
    main()

# eof-------------------------------------------------------------------------------------------------------------------
