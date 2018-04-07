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
    with open('get_tweets_query.cql', 'r') as qryHandle:
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

    with open('update_sentiment_query.cql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    tweetUpdate = session.prepare(qryText)

    counter = 0
    processed = 0
    batchSize = 500

    if len(tweets) > 0:
        for tweetId, tweetText in tweets.items():

            if counter == 0:
                startId = tweetId
                batch = BatchStatement()

            subjectivity, polarity = performSentimentAnalysis(tweetText)
            batch.add(tweetUpdate, (subjectivity, polarity, tweetId))
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
