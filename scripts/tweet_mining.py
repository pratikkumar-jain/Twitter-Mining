#!/usr/local/bin/python3

"""Script to get tweets based on a search query."""

import json
import jsonpickle
import os
import sys
import tweepy

from datetime import datetime
from zipfile import ZipFile


def mineTweet(root, api, drive):
    """Perform the mining operation."""
    searchQuery = 'empire state building'
    maxTweets = float('inf')
    tweetsPerQry = 100

    # Search gives tweets from current time to all the past but 100 per query
    # In the results tweet at index 0 is the latest one
    # In the results tweet at index 99 is the oldest one amongst the 100
    # This ID at index 99 becomes the max_id, so now the query will search
    # between beginning of time and max_id
    # In each loop max_id gets updated, restricting the search into past.

    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    if os.path.exists('start_point.txt'):
        with open('start_point.txt', 'r') as startHandle:
            sinceId = int(startHandle.read().strip()) + 1

        print('Restarting mining from {}'.format(sinceId))
    else:
        sinceId = None

    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching
    # the search query.
    max_id = -1.0

    tweetCount = 0

    logFile = root + '/log_{}.txt'.format(datetime
                                          .now()
                                          .strftime('%Y%m%d%H%M%S'))

    iteration = 0
    iterFiles = []

    with open(logFile, 'w') as logHandle:

        while tweetCount < maxTweets:

            fileId = datetime.now().strftime('%Y%m%d%H%M%S%f')
            outputFileName = root + '/tweets_{}.json'.format(fileId)

            lastSearch = False

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
                        print('No more tweets found')
                        lastSearch = True
                        break
                    else:
                        iterFiles.append(outputFileName)

                    f.write('[')
                    for tweet in new_tweets:
                        f.write(jsonpickle.encode(tweet._json,
                                                  unpicklable=False) + ',\n')
                    f.write('{}]')

                    tweetCount += len(new_tweets)

                    start_id = new_tweets[0].id
                    max_id = new_tweets[-1].id

                    logHandle.write('{} {} {}\n'
                                    .format(start_id, max_id, len(new_tweets)))

                    # Create start point for next run
                    if iteration == 0:
                        with open('start_point.txt', 'w') as startHandle:
                            startHandle.write(str(start_id))

                except tweepy.TweepError as e:
                    # Just exit if any error
                    print('some error : {}'.format(e))
                    break

            iteration += 1

            if iteration % 20 == 0 and len(iterFiles) > 0:

                zipFile = root + '/tweet_compressed_{}.zip'.format(
                    datetime.now().strftime('%Y%m%d%H%M%S'))

                print('Zipping {} tweet\'s data to {}'.format(tweetCount,
                                                              zipFile))

                with ZipFile(zipFile, 'w') as zipHandle:
                    for file in iterFiles:
                        zipHandle.write(file)
                        os.remove(file)

                iterFiles = []
                tweetCount = 0

                if drive:
                    with ZipFile(zipFile, 'rb') as zipHandle:
                        # 2. Create & upload a file text file.
                        uploaded = drive.CreateFile({'title': zipFile})
                        uploaded.SetContentString(zipHandle.read())
                        uploaded.Upload()
                        print('Uploaded file with ID {}'
                              .format(uploaded.get('id')))

        # Zip the remaining jsons if 20 are not created
        if lastSearch and len(iterFiles) > 0:

            zipFile = root + '/tweet_compressed_{}.zip'.format(
                datetime.now().strftime('%Y%m%d%H%M%S'))

            print('Zipping data to {}'.format(zipFile))

            with ZipFile(zipFile, 'w') as zipHandle:
                for file in iterFiles:
                    zipHandle.write(file)
                    os.remove(file)

        # Remove the only empty file if no tweet is found
        if lastSearch:
            os.remove(outputFileName)

def main():
    """Perform the initial setup."""
    # Code to upload credentials file
    colab = False

    if colab:

        from google.colab import auth
        from google.colab import files
        from oauth2client.client import GoogleCredentials
        from pydrive.auth import GoogleAuth
        from pydrive.drive import GoogleDrive

        uploaded = files.upload()

        for fn in uploaded.keys():
            with open('../credential.json', 'w') as fileHandle:
                fileHandle.write(uploaded[fn])

        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = GoogleCredentials.get_application_default()
        drive = GoogleDrive(gauth)

        root = 'data'
    else:
        root = '../data'
        drive = None

    with open('../credential.json', 'r') as fileHandle:
        credData = json.loads(fileHandle.read())

    # Create the auth object.
    authObj = tweepy.AppAuthHandler(credData['API_KEY'],
                                    credData['API_SECRET'])

    api = tweepy.API(authObj, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if not api:
        print('Authentication Problem')
        sys.exit(-1)
    else:
        # 1. Authenticate and create the PyDrive client.
        mineTweet(root, api, drive)


if __name__ == '__main__':
    main()
