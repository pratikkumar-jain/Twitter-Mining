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

   # support_index = tweetObj.support_index if (tweetObj.support_index or tweetObj.support_index != 0) else minSupport
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
