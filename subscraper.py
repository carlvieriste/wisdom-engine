import time

import praw
import yaml
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


def get_comment_data(comment):
    wanted_data = {}
    for at in comment_attributes:
        wanted_data[at] = getattr(comment, at)
    return wanted_data


reddit = praw.Reddit(client_id='cvB_tLtMnpg68w', client_secret="oYuhGLknTRDyjShh__tTCJykfj4",
                     password='Rougesay666666', user_agent='philosophy_scraper by /u/carlvieriste',
                     username='carlvieriste')

counter = 0

submission_id = '3jd7hj'
s = reddit.submission(id=submission_id)

# Get submission data
s_data = {}
for a in submission_attributes:
    s_data[a] = getattr(s, a)

author_id = s.author

# Get comment data
s_comments = []
for top_level_comment in s.comments:
    if isinstance(top_level_comment, MoreComments):
        continue  # Get only first page of comments

    # In case of a ama, comments are questions
    c_data = get_comment_data(top_level_comment)

    # Get replies from ama redditor (there should be a single one)
    replies = []
    for r in top_level_comment.replies:
        if r.author == author_id:  # Get only replies from ama redditor
            replies.append(get_comment_data(r))

    if len(replies) == 0:  # If the ama redditor has not replied, ignore question
        continue

    c_data['__0title'] = top_level_comment.body[0:100]
    c_data['__replies'] = replies
    s_comments.append(c_data)

    counter += 1
    if counter % 10 == 0:
        print(counter)

all_data = {
    'submission': s_data,
    'comments': s_comments
}

# print("Total submissions: {}".format(len(s_list)))

with open('{}_{}.yaml'.format(submission_id, time.time()), 'w') as file:
    yaml.dump(all_data, file)
