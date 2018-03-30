#!/usr/local/bin/python3

"""Script to get tweets based on a search query."""

import json
import sys
import tweepy


def main():
    """Perform the initial setup."""
    with open('../credential.json', 'r') as fileHandle:

        credData = json.loads(fileHandle.read())

    # Create the auth object.
    auth = tweepy.AppAuthHandler(credData['API_KEY'], credData['API_SECRET'])

    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    if not api:
        print("Authentication Problem")
        sys.exit(-1)

if __name__ == '__main__':
    main()
