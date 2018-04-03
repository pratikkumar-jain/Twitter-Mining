#!/usr/local/bin/python3

"""Script to build the repository from the extracted tweets."""

import json
import os
import shutil
import sys


from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from zipfile import ZipFile


def unzipTweets():
    """Unzip the compressed tweets."""
    if not os.path.exists('../data/processed'):
        os.makedirs('../data/processed')
    root = '../data/'
    for file in os.listdir(root):
        filename = os.fsdecode(file)
        if filename.endswith('.zip'):
            print('Unzipping file: {}'.format(filename))
            with ZipFile(root + filename, 'r') as zip_ref:
                zip_ref.extractall('../data')
            src = root + filename
            dest = '../data/processed'
            shutil.move(src, dest)


def buildDB():
    """Build the database."""
    # Create instance of local cassandra cluster

    cluster = Cluster()

    # Connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')

    # Creating dynamic CQL query
    qryText = None
    with open('insert_query.sql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    tweet_insert = session.prepare(qryText)
    root = '../data/data/'

    # Using a translation table to map everything outside of the BMP (emojis)
    # to the replacement character
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    for file in os.listdir(root):
        batch = BatchStatement()

        with open(root + file, 'r') as fileHandle:
            # batch.add(tweet_insert, (name, age))
            filedata = json.load(fileHandle)
            for data in filedata:
                try:
                    # Filtering non-bmp characters from tweet text
                    tweet_text = str(data.get('text')).translate(non_bmp_map)
                    if data.get('id_str'):
                        batch.add(tweet_insert, (data.get('id_str'),
                                                 tweet_text,
                                                 data.get('favorite_count'),
                                                 data.get('retweet_count'),
                                                 data.get('lang')))
                except Exception as exp:
                    print('Error: {}'.format(exp))
                    print(sys.exc_info())
            print('Processing Batch of file : {}'.format(file))
            session.execute(batch)
    shutil.rmtree('../data/data')


def main():
    """Initialize everything."""
    unzipTweets()

    if not os.path.exists('../data/data'):
        print("There are no new tweets to add to the database")
    else:
        buildDB()


if __name__ == '__main__':
    main()
