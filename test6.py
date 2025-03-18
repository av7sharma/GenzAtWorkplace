import pandas as pd
import nltk
import re
from nltk.corpus import stopwords

# Ensure necessary NLTK resources are downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Load data from the Excel file
file_path = "merged_reddit_data.xlsx"  # Change if necessary
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

# Save the themes to Excel
data.to_excel("reddit_themes_classified.xlsx", index=False)

# Get overarching themes summary
theme_counts = data["theme"].explode().value_counts().reset_index()
theme_counts.columns = ["Theme", "Count"]
theme_counts.to_excel("reddit_overarching_themes_classified.xlsx", index=False)

print("✅ Themes classified successfully! Check 'reddit_themes_classified.xlsx' for post-level themes and 'reddit_overarching_themes_classified.xlsx' for overarching themes.")
