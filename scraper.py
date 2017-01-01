import time
import yaml
import numpy as np
import praw
from praw.models import MoreComments

submission_attributes = ['created_utc',
                         'downs',
                         'fullname',
                         'id',
                         'likes',
                         'num_comments',
                         'num_reports',
                         'score',
                         'selftext',
                         'title',
                         'ups',
                         'user_reports']

comment_attributes = ['body',
                      'created_utc',
                      'controversiality',
                      'downs',
                      'fullname',
                      'id',
                      'is_root',
                      'likes',
                      'mod_reports',
                      'num_reports',
                      'parent_id',
                      'score',
                      'ups',
                      'user_reports']

reddit = praw.Reddit(client_id='cvB_tLtMnpg68w', client_secret="oYuhGLknTRDyjShh__tTCJykfj4",
                     password='Rougesay666666', user_agent='philosophy_scraper by /u/carlvieriste',
                     username='carlvieriste')

subreddit_name = 'confucianism'
# subreddit_name = 'askreligion'
subred = reddit.subreddit(subreddit_name)

s_list = []

counter = 0
for i, s in enumerate(subred.top(limit=None)):  # None: fetch as many as possible, typically max 1000
    # Get submission data
    s_data = {}
    for a in submission_attributes:
        s_data[a] = getattr(s, a)

    # Get comment data
    s_comments = []
    for top_level_comment in s.comments:
        if isinstance(top_level_comment, MoreComments):
            continue  # Get only first page of comments
        c_data = {}
        for a in comment_attributes:
            c_data[a] = getattr(top_level_comment, a)
        s_comments.append(c_data)

    s_data['__comments'] = s_comments
    s_list.append(s_data)

    counter += 1
    if counter % 10 == 0:
        print(counter)

print("Total submissions: {}".format(len(s_list)))

with open('{}_{}.yaml'.format(subreddit_name, time.time()), 'w') as file:
    yaml.dump(s_list, file)
