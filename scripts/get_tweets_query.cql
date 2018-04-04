SELECT tweet_id, tweet_text
FROM tweets
WHERE tweet_polarity = -10 and tweet_subjectivity = -10 ALLOW FILTERING
