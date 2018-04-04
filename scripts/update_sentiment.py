#!/usr/local/bin/python3

"""Script to update the sentiment values for tweets."""
"""which have not been analyzed or are newly added to database."""

from cassandra.cluster import Cluster
from textblob import TextBlob


def getTweets(session):
    """Get IDs and text for which analysis is pending."""
    tweets = {}

    # Creating dynamic CQL query
    qryText = None
    with open('get_tweets_query.sql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    results = session.execute(qryText)

    for result in results:
        tweets[result.tweet_id] = result.tweet_text

    return tweets


def performSentimentAnalysis(tweetText):
    """Analyze sentiment."""
    blob = TextBlob(tweetText)

    return blob.sentiment.subjectivity, blob.sentiment.polarity


def updateSentiment(tweetId, subjectivity, polarity):
    """Update tweet with sentiment."""


def main():
    """Initialize everything."""
    # Create instance of local cassandra cluster
    cluster = Cluster()

    # Connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')






if __name__ == '__main__':
    main()
