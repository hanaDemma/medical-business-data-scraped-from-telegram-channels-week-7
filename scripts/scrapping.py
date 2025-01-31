import os
import pandas as pd
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

async def scrapping(logging, api_id, api_hash, RAW_DATA_PATH, IMAGE_DATA_PATH):
  
    os.makedirs(RAW_DATA_PATH, exist_ok=True)
    os.makedirs(IMAGE_DATA_PATH, exist_ok=True)

    all_messages = []

    # Function to scrape a Telegram channel
    async def scrape_channel(channel_name, is_image_channel=False, target_valid_count=10):
        async with TelegramClient('session_name', api_id, api_hash) as client:
            valid_count = 0
            
            async for message in client.iter_messages(channel_name):
                # Check if the message has text and contains more than one line
                if message.text and message.text.count('\n') >= 1:  # More than one line
                    # Prepare the message data with channel name
                    msg_data = {
                        'channel_name': channel_name,  # Add channel name
                        'message_id': message.id,
                        'date': message.date.strftime('%Y-%m-%d %H:%M:%S'),
                        'text': message.text,
                        'image_path': None  # Initialize image path
                    }

                    # If it's an image channel, download images
                    if is_image_channel and message.media and isinstance(message.media, MessageMediaPhoto):
                        # Download the image
                        photo = await client.download_media(message.media, file=IMAGE_DATA_PATH)
                        msg_data['image_path'] = photo 
                        logging.info(f'Downloaded image: {photo} from message_id: {message.id}')

                    all_messages.append(msg_data)  # Append the message data to the list
                    valid_count += 1  # Increment the valid message count

                    # Stop if we've reached the desired number of valid messages
                    if valid_count >= target_valid_count:
                        break
                else:
                    logging.info(f'Ignored message_id {message.id} with less than two lines.')

    # List of channels to scrape
    text_channels = [
        'DoctorsET',
        'CheMed123',  # Include in text channels, but will handle images separately
        'lobelia4cosmetics',
        'yetenaweg',
        'EAHCI'
    ]

    image_channels = [
        'CheMed123',
        'lobelia4cosmetics'
    ]

    try:
        for channel in text_channels:
            is_image_channel = channel in image_channels
            await scrape_channel(channel, is_image_channel=is_image_channel, target_valid_count=10)

        # Save all messages to a single CSV file after scraping all channels
        if all_messages:
            df = pd.DataFrame(all_messages)
            df.to_csv(os.path.join(RAW_DATA_PATH, 'all_scraped_messages.csv'), index=False)
            logging.info(f'Scraped data from all channels and saved to all_scraped_messages.csv')
        else:
            logging.warning('No valid messages found in any channels.')
    except Exception as e:
        logging.error(f'An error occurred: {e}')