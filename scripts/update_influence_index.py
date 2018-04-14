#!/usr/local/bin/python3

"""Script to update the influence index for all tweets."""

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from textblob import TextBlob



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



def calculateNormalizedInfluenceIndex(maxInfluence, minInfluence, tweetObj):
    """Normalizing Number of followers"""
    normalized_influence_index = 100 * (tweetObj.user_followers_count - minInfluence) / (maxInfluence - minInfluence)
    return normalized_influence_index




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

    with open('update_influence_index_query.cql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    tweetUpdate = session.prepare(qryText)

    counter = 0
    processed = 0
    batchSize = 500

    # Counter for normalizing tweets
    max_influence_result = session.execute('select max(user_followers_count) as max_influence from tweets;')
    max_influence = max_influence_result.current_rows[0].max_influence
    min_influence_result = session.execute('select min(user_followers_count) as min_influence from tweets;')
    min_influence = min_influence_result.current_rows[0].min_influence

    print (max_influence)
    print (min_influence)

    tweetUpdate = session.prepare(qryText)

    for tweetId, tweetObj in tweets.items():

        if counter == 0:
            startId = tweetId
            batch = BatchStatement()

        normalized_ii_value = calculateNormalizedInfluenceIndex(max_influence, min_influence, tweetObj)

        batch.add(tweetUpdate, (normalized_ii_value, tweetId))
        processed += 1
        counter += 1

        if counter % batchSize == 0 or processed == len(tweets):
            endId = tweetId
            batchUpdate(batch, session, startId, endId, counter)
            counter = 0

if __name__ == '__main__':
    main()
