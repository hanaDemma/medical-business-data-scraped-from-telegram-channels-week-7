
# **Building a Data Warehouse for Ethiopian Medical Business Data**


## Project Overview

This project involves creating a data warehouse for Kara Solutions, which stores data on Ethiopian medical businesses scraped from Telegram channels. The objective is to enable insights into trends and patterns within the medical sector in Ethiopia. Key tasks included data scraping, cleaning, transformation, object detection, and API development for data access.

## Data Collection

Data was collected from Telegram channels using the Telethon library.

### Steps:

1. **Telethon API:** Connected to Telegram API to extract text and metadata.
2. **Logging:** Implemented to track the scraping process.
3. **Storage:** Temporarily stored raw data before processing.


## Data Cleaning and Transformation

Using DBT, I performed data cleaning and transformations:

1. **Data Cleaning:** Removed duplicates and handled missing values.
2. **Data Transformation:** Utilized DBT models to structure and transform data, ensuring consistency.

## **Technologies Used**

- **Python**: Main language for all scripts.
- **Telethon**: Used to scrape Telegram data.
- **Pandas**: For data manipulation and cleaning.
- **PostgreSQL**: Relational database to store cleaned data.
- **DBT (Data Build Tool)**: For transforming and loading data into the warehouse.


## Installation

1. **Clone the repository:**

   git clone https://github.com/hanaDemma/medical-business-data-scraped-from-telegram-channels-week-7.git

   cd Building-a-Data-Warehouse-to-store-data
2. pip install -r requirements.txt
3. **Setup PostgreSQL and DBT:**
   Configure your PostgreSQL database.

