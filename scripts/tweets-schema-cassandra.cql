CREATE KEYSPACE IF NOT EXISTS tweet_mining WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1};
USE tweet_mining;
DROP TABLE IF EXISTS tweets;
CREATE TABLE IF NOT EXISTS tweets(
 tweet_id text PRIMARY KEY,
 tweet_text text,
 search_query text,
 favorite_count int,
 retweet_count int,
 created_at text,
 lang text,
 geo text,
 place text,
 user_id text,
 user_followers_count int,
 user_friends_count int,
 user_statuses_count int,
 user_screen_name text,
 user_verified boolean,
 user_favourites_count int,
 support_index float,
 tweet_polarity float,
 tweet_subjectivity float
);
