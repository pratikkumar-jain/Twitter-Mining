import json
import enchant
from sklearn.feature_extraction.text import CountVectorizer
# from nltk.corpus import stopwords

# File Path : Change accordingly
filename = "/Users/pratik/Downloads/dataset/review.json"
output_text = []


# function to read a review and append it to the list
# if it is useful
def filereader(line):
    gdfJson = json.loads(line)
    if gdfJson['useful'] > 0:
        out = gdfJson['text'].replace('\n', '')
        output_text.append(out)


count = 0
with open(filename, 'r') as f:
    for line in f:
        count += 1
        if count < 10000:
            filereader(line)
        else:
            break

# package to check if a word is in Dictionary
d = enchant.Dict("en_US")

output_text2 = []
for reviews in output_text:
    filtered_words = []
    for word in reviews:
        if d.check(word):
            filtered_words.append(word)
    output_text2.append(''.join(filtered_words))

# function to create Bag of Words by removing stop words
vectorizer = CountVectorizer(stop_words='english')
vectorizer.fit_transform(output_text2).todense()
print(vectorizer.vocabulary_)
