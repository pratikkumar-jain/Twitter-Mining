#!/usr/local/bin/python3

"""Script to get tweets based on a search query."""

import json
import jsonpickle
import os
import sys
import tweepy

from datetime import datetime
from google.colab import auth
from google.colab import files
from oauth2client.client import GoogleCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from zipfile import ZipFile


def mineTweet(api, drive):
    """Perform the mining operation."""
    searchQuery = 'empire state building'
    maxTweets = float('inf')
    tweetsPerQry = 100

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching
    # the search query.
    max_id = -1.0

    tweetCount = 0

    logFile = '../data/log.txt'

    iteration = 0
    iterFiles = []

    with open(logFile, 'w') as logHandle:

        logHandle.write('Downloading max {0} tweets\n'.format(maxTweets))

        while tweetCount < maxTweets:

            fileId = datetime.now().strftime('%Y%m%d%H%M%S')
            outputFileName = '../data/tweets_{}.txt'.format(fileId)
            iterFiles.append(outputFileName)

            with open(outputFileName, 'w') as f:
                try:
                    if (max_id <= 0):
                        if (not sinceId):
                            new_tweets = api.search(q=searchQuery,
                                                    count=tweetsPerQry)
                        else:
                            new_tweets = api.search(q=searchQuery,
                                                    count=tweetsPerQry,
                                                    since_id=sinceId)
                    else:
                        if (not sinceId):
                            new_tweets = api.search(q=searchQuery,
                                                    count=tweetsPerQry,
                                                    max_id=str(max_id - 1))
                        else:
                            new_tweets = api.search(q=searchQuery,
                                                    count=tweetsPerQry,
                                                    max_id=str(max_id - 1),
                                                    since_id=sinceId)
                    if not new_tweets:
                        logHandle.write('No more tweets found')
                        break

                    for tweet in new_tweets:
                        f.write(jsonpickle.encode(tweet._json,
                                                  unpicklable=False) + '\n')

                    tweetCount += len(new_tweets)

                    logHandle.write('Downloaded {} tweets in current query\n'
                                    .format(len(new_tweets)))

                    max_id = new_tweets[-1].id

                    logHandle.write('{} {}\n'.format(max_id, sinceId))

                except tweepy.TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break

            iteration += 1

            if iteration % 5 == 0:
                zipFile = 'tweet_compressed_{}.zip'.format(
                    datetime.now().strftime('%Y%m%d%H%M%S'))

                with ZipFile(zipFile, 'w') as zipHandle:
                    for file in iterFiles:
                        zipHandle.write(file)
                        os.remove(file)

                    zipHandle.write('../data/log.txt')
                    os.remove('../data/log.txt')

                iterFiles = []

                with ZipFile(zipFile, 'rb') as zipHandle:
                    # 2. Create & upload a file text file.
                    uploaded = drive.CreateFile({'title': zipFile})
                    uploaded.SetContentString(zipHandle.read())
                    uploaded.Upload()
                    print('Uploaded file with ID {}'
                          .format(uploaded.get('id')))


def main():
    """Perform the initial setup."""
    # Code to upload credentials file
    uploaded = files.upload()

    for fn in uploaded.keys():
        with open('../credential.json', 'w') as fileHandle:
            fileHandle.write(uploaded[fn])

    with open('../credential.json', 'r') as fileHandle:
        credData = json.loads(fileHandle.read())

    # Create the auth object.
    authObj = tweepy.AppAuthHandler(credData['API_KEY'],
                                    credData['API_SECRET'])

    api = tweepy.API(authObj, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if not api:
        print("Authentication Problem")
        sys.exit(-1)
    else:
        # 1. Authenticate and create the PyDrive client.
        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        drive = GoogleDrive(gauth)
        mineTweet(api, drive)


if __name__ == '__main__':
    main()
