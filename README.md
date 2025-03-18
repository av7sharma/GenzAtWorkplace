# GenzAtWorkplace

## Overview

This project analyzes workplace sentiment based on discussions extracted from Reddit. Using Natural Language Processing (NLP) techniques, the system classifies posts into key workplace themes, performs sentiment and urgency analysis, and generates structured insights.

## Features

Reddit Data Scraping: Collects workplace-related discussions from multiple subreddits.

Text Preprocessing: Cleans and processes text by removing stopwords and special characters.

Thematic Classification: Categorizes posts into predefined workplace themes:

CF (Compensation & Fairness)

MSR (Managerial Support & Recognition)

MWGO (Meaningful Work & Growth Opportunities)

WLFOC (Work-Life Flexibility & Organizational Culture)

Additional themes: JSS, WDI, EWMH, RHW

Sentiment & Emotion Analysis: Identifies emotions in text using a deep learning model.

Urgency & Actionability Detection: Determines if a post is actionable or expresses urgency.

Data Export: Saves classified themes, sentiment, and urgency analysis into structured Excel files for further research.

## Files & Components

### 1. Reddit Data Collection (reddit_crawler_final.py)

Uses praw to scrape posts from subreddits.

Stores data in an SQLite database (reddit_data.db).

### 2. Text Processing & Thematic Classification (test6.py)

Reads scraped data and preprocesses text.

Classifies posts into workplace themes.

Exports results to reddit_themes_classified.xlsx and reddit_overarching_themes_classified.xlsx.

### 3. Sentiment & Urgency Analysis (test9.py)

Performs emotion classification using a deep learning model.

Analyzes urgency and actionability based on keyword matching.

Saves processed data in reddit_themes_emotion_urgency.xlsx.

Generates summary reports in reddit_overarching_themes_emotion.xlsx and reddit_overarching_themes_urgency.xlsx.

## Installation & Setup

### Prerequisites:
Python 3.x

### Required Python libraries:
```bash
pip install praw pandas nltk transformers openpyxl
```

### Steps to Run:

Run the Reddit Scraper to collect data:
```bash
python3 reddit_crawler_final.py
```

Classify Workplace Themes:
```bash
python3 test6.py
```

Perform Sentiment & Urgency Analysis:
```bash
python test9.py
```

## Check Generated Reports:

reddit_themes_classified.xlsx

reddit_overarching_themes_classified.xlsx

reddit_themes_emotion_urgency.xlsx

reddit_overarching_themes_emotion.xlsx

reddit_overarching_themes_urgency.xlsx

## Output & Insights

Identifies dominant workplace concerns based on discussion frequency.
![Alt Text](output (2).png)
Highlights sentiment trends (e.g., frustration with compensation & managerial support).
![Alt Text](output (3).png)
Maps urgency levels, helping organizations prioritize key workplace issues.
![Alt Text](output (4).png)
Enables researchers to analyze employee perceptions of work-life balance, growth, and well-being.

## Future Enhancements

Implement topic modeling for more refined categorization.
Introduce time-based trend analysis for tracking evolving discussions.
Improve sentiment analysis accuracy by incorporating contextual understanding.

