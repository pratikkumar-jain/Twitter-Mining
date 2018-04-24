1#select tweet_id from tweets WHERE normalized_review_relevance_index >= 0.003 AND normalized_review_relevance_index <= 0.02 AND lang ='en' AND retweeted = False allow filtering
2#select tweet_id from tweets WHERE normalized_support_index <= 0.000008 AND lang ='en' AND retweeted = False allow filtering
3#select tweet_id from tweets WHERE normalized_support_index >= 0.005 AND lang ='en' AND retweeted = False allow filtering
4#select tweet_id from tweets WHERE normalized_influential_index <= 0.002 AND lang ='en' AND retweeted = False allow filtering
5#select tweet_id from tweets WHERE tweet_polarity >= -1 AND tweet_polarity <= -0.3 AND lang ='en' AND retweeted = False allow filtering
6#select tweet_id from tweets WHERE tweet_polarity >= 0.7 AND lang ='en' AND retweeted = False allow filtering
7#select tweet_id from tweets WHERE tweet_subjectivity >= 0.25 AND tweet_subjectivity <= 0.5 AND lang ='en' AND retweeted = False allow filtering
