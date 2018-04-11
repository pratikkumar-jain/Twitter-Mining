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


