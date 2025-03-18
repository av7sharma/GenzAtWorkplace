import pandas as pd
import nltk
import re
from nltk.corpus import stopwords
from transformers import pipeline

# Ensure necessary NLTK resources are downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Load data from the Excel file
file_path = "reddit_data.xlsx"  # Change if necessary
data = pd.read_excel(file_path)

# Check if required columns exist
if data.shape[1] < 4:
    print("❌ Error: Excel file does not have at least 4 columns with title and text in 3rd and 4th columns.")
    exit()

# Extract title and text from the correct columns
data["title"] = data.iloc[:, 2]
data["text"] = data.iloc[:, 3]

# Combine title and text into a single column
data["content"] = data["title"] + " " + data["text"]

# Function to preprocess text
def preprocess_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove special characters
    text = " ".join([word for word in text.split() if word not in stop_words])
    return text

# Apply preprocessing
data["processed_text"] = data["content"].apply(preprocess_text)

# Define predefined categories
categories = {
    "CF": ["salary", "compensation", "pay", "wage", "fairness", "benefits"],
    "MSR": ["manager", "leadership", "recognition", "support", "feedback", "appreciation"],
    "MWGO": ["growth", "career", "promotion", "learning", "opportunity", "development"],
    "WLFOC": ["work-life", "balance", "flexibility", "culture", "remote", "wellbeing"],
    "JSS": ["job security", "layoffs", "stability", "permanency", "long-term", "tenure"],
    "WDI": ["diversity", "inclusion", "equity", "belonging", "representation", "bias"],
    "EWMH": ["stress", "burnout", "mental health", "well-being", "therapy", "mindfulness"],
    "RHW": ["remote work", "hybrid", "telecommute", "work from home", "flexibility", "virtual"]
}

# Function to classify text based on categories
def classify_text(text):
    category_matches = {category: any(word in text for word in keywords) for category, keywords in categories.items()}
    return [category for category, match in category_matches.items() if match]

# Classify posts into categories
data["theme"] = data["processed_text"].apply(classify_text)

# Emotion Analysis
emotion_pipeline = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=False)

def analyze_emotion(text):
    try:
        result = emotion_pipeline(text[:512])  # Truncate text if too long
        return result[0]['label']
    except:
        return "Unknown"

data["emotion"] = data["processed_text"].apply(analyze_emotion)

# Urgency & Actionability Analysis
def analyze_urgency(text):
    urgency_keywords = ["urgent", "immediate", "asap", "crisis", "emergency", "critical"]
    action_keywords = ["should", "must", "need to", "require", "mandatory", "important"]
    contains_urgency = any(word in text for word in urgency_keywords)
    contains_action = any(word in text for word in action_keywords)
    
    if contains_urgency and contains_action:
        return "High Urgency & Actionable"
    elif contains_urgency:
        return "High Urgency"
    elif contains_action:
        return "Actionable"
    else:
        return "General Discussion"

data["urgency_actionability"] = data["processed_text"].apply(analyze_urgency)

# Save the themes, emotion, and urgency analysis to Excel
data.to_excel("reddit_themes_emotion_urgency.xlsx", index=False)

# Get overarching themes summary with emotion and urgency breakdown
theme_emotion_counts = data.explode("theme").groupby(["theme", "emotion"]).size().unstack(fill_value=0)
theme_urgency_counts = data.explode("theme").groupby(["theme", "urgency_actionability"]).size().unstack(fill_value=0)

theme_emotion_counts.to_excel("reddit_overarching_themes_emotion.xlsx")
theme_urgency_counts.to_excel("reddit_overarching_themes_urgency.xlsx")

print("✅ Themes, emotion, and urgency analysis completed! Check 'reddit_themes_emotion_urgency.xlsx' for post-level data and 'reddit_overarching_themes_emotion.xlsx' & 'reddit_overarching_themes_urgency.xlsx' for summarized insights.")

