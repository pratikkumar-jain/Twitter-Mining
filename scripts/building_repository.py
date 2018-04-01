#!/usr/local/bin/python3

"""Script to build the repository from the extracted tweets"""

import json
import jsonpickle
import os
import sys
from zipfile import ZipFile
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
import re
import datetime
from cassandra.util import uuid_from_time, datetime_from_uuid1


def unzipTweets():
    """Unzip the compressed tweets"""
    root="../data/"
    for file in os.listdir(root):
        filename = os.fsdecode(file)
        if filename.endswith(".zip"):
            print("unzipping ",filename)
            with ZipFile(root+filename,"r") as zip_ref:
                zip_ref.extractall("../data")
    
def buildDB():
    """Build the database"""
    #create instance of local cassandra cluster
    cluster = Cluster()
    #connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')
    #creating dynamic CQL query
    tweet_insert = session.prepare("INSERT INTO tweets (tweet_id, tweet_text, favorite_count, retweet_count) VALUES (?, ?, ?, ?)")
    root="../data/data/"
    #Using a translation table to map everything outside of the BMP (emojis) to the replacement character
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    for file in os.listdir(root):
        batch = BatchStatement()
        with open(root+file,"r") as fileHandle:
            #batch.add(tweet_insert, (name, age))
            filedata =json.load(fileHandle)
            for data in filedata:
                try:
                    #filtering non-bmp characters from tweet text
                    tweet_text = str(data.get('text')).translate(non_bmp_map)
                    if data.get('id_str'):
                        batch.add(tweet_insert,(data.get('id_str'),tweet_text,data.get('favorite_count'),data.get('retweet_count')))
                except:
                    print (sys.exc_info())
            print("Processing Batch of file : ",file)
            session.execute(batch)
            
def main():
    unzipTweets()
    buildDB()

if __name__ == '__main__':
    main()
