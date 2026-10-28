# preprocessing.py
import pandas as pd
import re
import warnings
import nltk
from nltk.corpus import stopwords
import spacy

# Suppress warnings
warnings.filterwarnings("ignore")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Download stopwords quietly (won't print paths)
nltk.download('stopwords', quiet=True)
nltk.data.path.append('./nltk_data')  # point NLTK to local folder
stop_words = set(stopwords.words('english'))

# Function to clean text
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Function to lemmatize text
def lemmatize(text):
    doc = nlp(text)
    lemmas = [token.lemma_ for token in doc if token.is_alpha and token.text not in stop_words]
    return " ".join(lemmas)

# Function to preprocess DataFrame
def preprocess_df(df, text_col="description"):
    df = df.copy()
    df['clean_text'] = df[text_col].fillna("").map(clean_text)
    df['lemma_text'] = df['clean_text'].map(lemmatize)
    return df

if __name__ == "__main__":
    # Example usage
    df = pd.DataFrame({
        "description": [
            "We are hiring a Python developer!",
            "Data science and ML skills required."
        ]
    })
    df_clean = preprocess_df(df)
    print(df_clean)