import pandas as pd
import logging
import re
import os
import emoji

# Ensure logs folder exists
os.makedirs("../logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/data_cleaning.log"),
        logging.StreamHandler()
    ]
)

def load_csv(file_path):
    """ Load CSV file into a Pandas DataFrame. """
    try:
        df = pd.read_csv(file_path)
        logging.info(f"✅ CSV file '{file_path}' loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Error loading CSV file: {e}")
        raise

def extract_emojis(text):
    """ Extract emojis from text, return 'No emoji' if none found. """
    emojis = ''.join(c for c in text if c in emoji.EMOJI_DATA)
    return emojis if emojis else "No emoji"

def remove_emojis(text):
    """ Remove emojis from the message text. """
    return ''.join(c for c in text if c not in emoji.EMOJI_DATA)

def extract_youtube_links(text):
    """ Extract YouTube links from text. """
    youtube_pattern = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"
    links = re.findall(youtube_pattern, text)
    return ', '.join(links) if links else "No YouTube link"

def remove_youtube_links(text):
    """ Remove YouTube links from message text. """
    youtube_pattern = r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+"
    return re.sub(youtube_pattern, '', text).strip()

def clean_text(text):
    """ Standardize text by removing newline characters and extra spaces. """
    if pd.isna(text):
        return "No text"
    return re.sub(r'\n+', ' ', text).strip()

def clean_dataframe(df):
    """ Perform all cleaning and standardization steps. """
    try:
        df = df.drop_duplicates(subset=["message_id", "channel_name", "date"]).copy()
        logging.info("✅ Duplicates removed.")

        # ✅ Convert 'date' to datetime format
        df.loc[:, 'date'] = pd.to_datetime(df['date'], errors='coerce')
        df.loc[:, 'date'] = df['date'].where(df['date'].notna(), None)
        logging.info("✅ Date column formatted.")

        # ✅ Fill missing values
        df.loc[:, 'text'] = df['text'].fillna("No text")
        df.loc[:, 'image_path'] = df['image_path'].fillna("No image")
        logging.info("✅ Missing values filled.")

        # ✅ Clean text columns
        df.loc[:, 'text'] = df['text'].apply(clean_text)
        logging.info("✅ Text column cleaned.")

        # ✅ Extract and remove emojis
        df.loc[:, 'emoji_used'] = df['text'].apply(extract_emojis)
        df.loc[:, 'text'] = df['text'].apply(remove_emojis)
        logging.info("✅ Emojis processed.")

        # ✅ Extract and remove YouTube links
        df.loc[:, 'youtube_links'] = df['text'].apply(extract_youtube_links)
        df.loc[:, 'text'] = df['text'].apply(remove_youtube_links)
        logging.info("✅ YouTube links processed.")

        # ✅ Rename columns for consistency
        df = df.rename(columns={
            "channel_name": "channel_title",
            "date": "message_date",
            "text": "message",
            "image_path": "media_path",
        })

        logging.info("✅ Data cleaning completed successfully.")
        return df
    except Exception as e:
        logging.error(f"❌ Data cleaning error: {e}")
        raise

def save_cleaned_data(df, output_path):
    """ Save cleaned data to a CSV file. """
    try:
        df.to_csv(output_path, index=False)
        logging.info(f"✅ Cleaned data saved to '{output_path}'.")
        print(f"✅ Cleaned data saved to '{output_path}'.")
    except Exception as e:
        logging.error(f"❌ Error saving cleaned data: {e}")
        raise
