import praw
import pandas as pd
import sqlite3
import time
import random

# Reddit API Authentication (Replace with your credentials)
reddit = praw.Reddit(
    client_id='TftPqJozeDudRvMUQJM4IA',
    client_secret='MZb_vhojCiSTJFz6mHIChDuD0bwkNg',
    user_agent='GenZ_Workplace_Crawler'
)

# SQLite Database Setup
db_connection = sqlite3.connect("reddit_data.db")
cursor = db_connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS reddit_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subreddit TEXT,
                    title TEXT,
                    text TEXT,
                    upvotes INTEGER,
                    comments INTEGER)''')
db_connection.commit()

def fetch_reddit_posts(subreddit_name, limit=100):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        posts = []
        for post in subreddit.hot(limit=limit):
            posts.append((subreddit_name, post.title, post.selftext, post.score, post.num_comments))
            time.sleep(random.uniform(2, 5))  # Avoid rate limits
        return posts
    except Exception as e:
        print(f"Skipping subreddit {subreddit_name}: {e}")
        return []

def save_to_database(posts):
    if posts:
        cursor.executemany("INSERT INTO reddit_posts (subreddit, title, text, upvotes, comments) VALUES (?, ?, ?, ?, ?)", posts)
        db_connection.commit()
        print(f"Saved {len(posts)} posts to database.")
    else:
        print("No posts to save.")

# Define subreddits to scrape
subreddits = [
    'Workplace',
    'OfficePolitics',
    'antiwork',
    'GenZ',
    'entrepreneur',
    'productivity'
]

# Fetch and store subreddit data in SQLite
for sub in subreddits:
    posts = fetch_reddit_posts(sub, limit=100)
    save_to_database(posts)

# Close database connection
db_connection.close()
print("Reddit data collection complete.")

