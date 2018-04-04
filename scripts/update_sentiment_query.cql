UPDATE tweets
SET
  tweet_subjectivity = ?,
  tweet_polarity = ?
WHERE tweet_id = ?
