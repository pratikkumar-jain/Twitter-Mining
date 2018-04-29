#!/usr/local/bin/python3
"""Script to calculate the resutls for all indices combined."""
# import pandas as pd

from cassandra.cluster import Cluster


def getTweets(session, queryText):
    """Get all tweets with all fields."""
    results = session.execute(queryText)
    res = set(['\'' + str(result.tweet_id) + '\'' for result in results])
    print(len(res))
    return res


def getTweetText(session, ids):
    """Get all tweets with all fields."""
    params = ','.join(ids)
    qryText = "SELECT * FROM tweets WHERE tweet_id IN ({})".format(params)
    results = session.execute(qryText)
    return results


def main():
    """Process the final formula."""
    # Create instance of local cassandra cluster
    cluster = Cluster()

    # Connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')

    tweetIdDict = {}

    with open('finalformula.cql', 'r') as qryHandle:
        for line in qryHandle:
            key, query = line.strip().split("#")
            ids = getTweets(session, query)
            tweetIdDict[int(key)] = ids

    finalSet = tweetIdDict[1] & \
        (tweetIdDict[2] | tweetIdDict[3]) & \
        tweetIdDict[4] & \
        (tweetIdDict[5] | tweetIdDict[6]) & \
        tweetIdDict[7]

    print('Total tweets: {}'.format(len(finalSet)))
    result = getTweetText(session, list(finalSet))

    goodTweets = [(twt.tweet_text, len(twt.tweet_text)) for twt in result]
    smallSet = sorted(goodTweets, key=lambda x: -x[1])[:25]

    for tweet in smallSet:
        print(tweet[0])

    # tweetDataFrame = pd.DataFrame(result)
    # print(tweetDataFrame.head(10))

if __name__ == '__main__':
    main()
