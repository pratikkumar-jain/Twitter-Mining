#!/usr/local/bin/python3

"""Script to update the review relevance index for all tweets."""

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from textblob import TextBlob
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import pandas as pd
import pdb
import json
from pprint import pprint

def getTweets(session):
    """Get all tweets with all fields."""
    tweets = {}

    # Creating dynamic CQL query
    qryText = None
    with open('get_all_fields_tweets_query.cql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    results = session.execute(qryText)

    for result in results:
        tweets[result.tweet_id] = result

    return tweets

def processTweet(tweet_txt):

    # TODO: Expand tweet
    tweetExpansion_dict = json.load(open('../data/dictionary_tweetExpansion.json'))
    print('expansion dict',tweetExpansion_dict)
    # Remove stop words
    # Lemmatize

    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()

    processed_tweet = []

    # for word in tokenizer.tokenize(tweet_txt):
    #     if english_dict.check(word) and not word.isdigit():
    #         lemmatizer.lemmatize(word)
    #         processed_tweet.append(word.lower())
    for word in tokenizer.tokenize(tweet_txt):
        if word in tweetExpansion_dict:
            word=tweetExpansion_dict[word]
            print('new word',word)
        lemmatizer.lemmatize(word)
        processed_tweet.append(word.lower())
    return processed_tweet

def calculateReviewRelevanceIndex(tweetObj, df):

    tweet_txt = processTweet(tweetObj.tweet_text)

    if not tweet_txt:
        return None

    tweet_score = 0
    for word in tweet_txt:
        review_record = df.loc[df['word'] == word]
        tweet_score += 0 if review_record.empty else review_record['normalized_count']

    return tweet_score / len(tweet_txt)

def calculateNormalizedReviewRelevanceIndex(max_value, min_value, tweetObj):

    review_relevance_index = tweetObj.review_relevance_index if (tweetObj.review_relevance_index and tweetObj.review_relevance_index >= 0.0 and tweetObj.review_relevance_index <=1.0) else min_value
    normalized_review_relevance_index = (review_relevance_index - min_value) / (max_value - min_value)

    return normalized_review_relevance_index

def batchUpdate(batch, session, startId, endId, counter):
    """Update sentiment in batches."""
    try:
        print('Processing Batch of {} {} {}'.format(
            counter, startId, endId), end=', ')
        session.execute(batch)
        print('Update Success')
    except Exception as exp:
        print('Exception in updating: {}, Update Failed'.format(exp))


def main():
    """Initialize everything."""

    df = pd.read_pickle('../data/yelp_bag_of_review_words.pkl')

    # Create instance of local cassandra cluster
    cluster = Cluster()

    # Connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')

    tweets = getTweets(session)

    with open('update_review_relevance_index_query.cql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    tweetUpdate = session.prepare(qryText)

    counter = 0
    processed = 0
    batchSize = 500

    if len(tweets) > 0:
        for tweetId, tweetObj in tweets.items():

            if counter == 0:
                startId = tweetId
                batch = BatchStatement()

            review_relevance = calculateReviewRelevanceIndex(tweetObj, df)

            batch.add(tweetUpdate, (review_relevance, tweetId))
            processed += 1
            counter += 1

            if counter % batchSize == 0 or processed == len(tweets):
                endId = tweetId
                batchUpdate(batch, session, startId, endId, counter)
                counter = 0

    else:
        print('No tweets to process')

    # Reset counter for normalizing tweets
    max_result = session.execute('select max(review_relevance_index) as max_value from tweets where review_relevance_index >=0.0 and review_relevance_index <= 1.0 allow filtering;')
    max_value = max_result.current_rows[0].max_value
    min_result = session.execute('select min(review_relevance_index) as min_value from tweets where review_relevance_index >=0.0 and review_relevance_index <= 1.0 allow filtering;')
    min_value = min_result.current_rows[0].min_value

    qryText = qryText.replace('review_relevance_index', 'normalized_review_relevance_index')
    tweetUpdate = session.prepare(qryText)

    counter = 0
    for tweetId, tweetObj in tweets.items():

        if counter == 0:
            startId = tweetId
            batch = BatchStatement()

        normalized_review_relevance = calculateNormalizedReviewRelevanceIndex(max_value, min_value, tweetObj)

        batch.add(tweetUpdate, (normalized_review_relevance, tweetId))
        processed += 1
        counter += 1

        if counter % batchSize == 0 or processed == len(tweets):
            endId = tweetId
            batchUpdate(batch, session, startId, endId, counter)
            counter = 0

if __name__ == '__main__':
    main()
