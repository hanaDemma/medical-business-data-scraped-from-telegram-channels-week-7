-- models/final_messages.sql

SELECT *
FROM {{ ref('all_scraped_messages') }}
