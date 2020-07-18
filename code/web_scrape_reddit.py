# Script used to scrape posts from two subreddits (LifeProTips and UnethicalLifeProTips)

# Imports
import pandas as pd
import datetime as dt
import time
import requests

# Scraping Function
## Function Written by Mahdi
## Time window modified to be in hours

def query_pushshift(subreddit, kind = 'submission', hour_window = 24, n = 5):
    SUBFIELDS = ['title', 'selftext', 'subreddit', 'created_utc', 'author', 'num_comments', 'score', 'is_self']
    
    # establish base url and stem
    BASE_URL = f"https://api.pushshift.io/reddit/search/{kind}" # also known as the "API endpoint" 
    stem = f"{BASE_URL}?subreddit={subreddit}&size=500" # always pulling max of 500
    
    # instantiate empty list for temp storage
    posts = []
    
    # implement for loop with `time.sleep(2)`
    for i in range(1, n + 1):
        URL = "{}&after={}h".format(stem, hour_window * i)
        print("Querying from: " + URL)
        response = requests.get(URL)
        assert response.status_code == 200
        mine = response.json()['data']
        df = pd.DataFrame.from_dict(mine)
        posts.append(df)
        time.sleep(3) 
    
    # pd.concat storage list
    full = pd.concat(posts, sort=False)
    
    # if submission
    if kind == "submission":
        # select desired columns
        full = full[SUBFIELDS]
        # drop duplicates
        full.drop_duplicates(inplace = True)
        # select `is_self` == True
        full = full.loc[full['is_self'] == True]

    # create `timestamp` column
    full['timestamp'] = full["created_utc"].map(dt.date.fromtimestamp)
    
    print("Query Complete!")    
    return full 

# Subreddit 1: Life Pro Tips
## Will scrape 12 hours' worth of data in each request
life_pro_tips = query_pushshift('LifeProTips', kind = 'submission', hour_window = 12, n = 30)

# Subreddit 2:
## Will oversample unethical LPTs to be able to remove 'Requests'
## Will scrape 168 hours (1 week) in each request
ue_life_pro_tips = query_pushshift('UnethicalLifeProTips', kind = 'submission', hour_window = 168, n = 40)

# Concatenate Data Frames
both_subreddits = pd.concat([life_pro_tips, ue_life_pro_tips])

# Export to CSV
both_subreddits.to_csv('../data/subreddits.csv')
print('Data has been exported.')
