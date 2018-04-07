#!/usr/local/bin/python3

"""Script to update the support index for all tweets."""

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from textblob import TextBlob
import pdb

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


def calculateSupportIndex(tweetObj):

    retweet_factor = 1.2
    retweet_count = tweetObj.retweet_count if tweetObj.retweet_count > 0 else 1
    fav_count = tweetObj.user_favourites_count if tweetObj.user_favourites_count > 0 else 1
    past_tweet_count = tweetObj.user_statuses_count if tweetObj.user_statuses_count > 0 else 1

    support_index = (retweet_count * retweet_factor + fav_count) / past_tweet_count

    return support_index

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
    # Create instance of local cassandra cluster
    cluster = Cluster()

    # Connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')

    tweets = getTweets(session)

    with open('update_support_index_query.cql', 'r') as qryHandle:
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

            si_value = calculateSupportIndex(tweetObj)

            batch.add(tweetUpdate, (si_value, tweetId))
            # batch.add(tweetUpdate, ('normalized_support_index', si_value, tweetId))
            processed += 1
            counter += 1

            if counter % batchSize == 0 or processed == len(tweets):
                endId = tweetId
                batchUpdate(batch, session, startId, endId, counter)
                counter = 0

    else:
        print('No tweets to process')

if __name__ == '__main__':
    main()
