CREATE KEYSPACE IF NOT EXISTS tweet_mining WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};
USE tweet_mining;
DROP TABLE IF EXISTS tweets;
CREATE TABLE IF NOT EXISTS tweets(
 tweet_id text PRIMARY KEY,
 tweet_text text,
 search_query text,
 favorite_count int,
 retweet_count int,
 created_at timestamp,
 lang text,
 tweet_polarity float,
 tweet_subjectivity float
);
