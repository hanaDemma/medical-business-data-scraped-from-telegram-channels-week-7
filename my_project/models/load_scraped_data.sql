-- models/load_scraped_data.sql

-- This model loads the scraped messages from the CSV file
with raw_data as (
    select *
    from {{ ref('all_scraped_messages') }}
    where message_id is not null
)

select distinct
    message_id,
    date,
    text,
    image_path,
    channel_name
from raw_data
