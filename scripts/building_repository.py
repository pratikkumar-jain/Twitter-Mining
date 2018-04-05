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
    with open('insert_query.cql', 'r') as qryHandle:
        qryText = qryHandle.read().strip()

    root = '../data/data/'

    # Using a translation table to map everything outside of the BMP (emojis)
    # to the replacement character
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    for file in os.listdir(root):
        batch = BatchStatement()
        search_query = "from filename"
        tweet_insert = session.prepare(qryText)
        with open(root + file, 'r') as fileHandle:
            # batch.add(tweet_insert, (name, age))
            filedata = json.load(fileHandle)
            for data in filedata:
                try:
                    # Filtering non-bmp characters from tweet text
                    tweet_text = str(data.get('text')).translate(non_bmp_map)
                    if data.get('id_str'):
                        if(data.get('geo')):
                            coords = str(data.get('geo')['coordinates'][0])+','+str(data.get('geo')['coordinates'][1])
                        else:
                            coords = 'x,y'
                        if data.get('place'):
                            place = data.get('place')['full_name']
                        else:
                            place = 'place'
                        batch.add(tweet_insert, (data.get('id_str'),
                                                 tweet_text,
                                                 search_query,
                                                 data.get('favorite_count'),
                                                 data.get('retweet_count'),
                                                 data.get('lang'),
                                                 coords,
                                                 place,
                                                 data.get('user').get('id_str'),
                                                 data.get('user').get('followers_count'),
                                                 data.get('user').get('friends_count'),
                                                 data.get('user').get('statuses_count'),
                                                 data.get('user').get('screen_name'),
                                                 data.get('user').get('verified'),
                                                 data.get('user').get('favourites_count')))
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
