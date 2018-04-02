from cassandra.cluster import Cluster
from sklearn.feature_extraction.text import CountVectorizer

def createBagofWords():
    output_text = []
    cluster = Cluster()
    #connect to 'tweet_mining' keyspace
    session = cluster.connect('tweet_mining')
    rows = session.execute("SELECT tweet_id,tweet_text FROM tweets where lang='en' ALLOW FILTERING")
    for row in rows:
        output_text.append(row[1])
    vectorizer = CountVectorizer()
    print( vectorizer.fit_transform(output_text).todense() )
    print( vectorizer.vocabulary_ )
    
def main():
    createBagofWords()

if __name__ == '__main__':
    main()

