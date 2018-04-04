#!/usr/local/bin/python3

"""Script to update the sentiment values for tweets."""
"""which have not been analyzed or are newly added to database."""

from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
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

    print('{} Tweets found'.format(len(tweets)))
    return tweets


def performSentimentAnalysis(tweetText):
    """Analyze sentiment."""
    blob = TextBlob(tweetText)

    return blob.sentiment.subjectivity, blob.sentiment.polarity


def main():
    """Initialize everything."""
    # Create instance of local cassandra cluster
    cluster = Cluster()

    # Connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')

    tweets = getTweets(session)

    batch = BatchStatement()

    with open('update_sentiment_query.sql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    tweetUpdate = session.prepare(qryText)

    for tweetId, tweetText in tweets.values():
        subjectivity, polarity = performSentimentAnalysis(tweetText)
        batch.add(tweetUpdate, (tweetId, subjectivity, polarity))

    try:
        print('Processing Batch Update for {} tweets'.format(len(tweets)))
        session.execute(batch)
        print('Update Success')
    except Exception as exp:
        print('Exception in updating: {}'.format(exp))
        print('Update Failed')

if __name__ == '__main__':
    main()
