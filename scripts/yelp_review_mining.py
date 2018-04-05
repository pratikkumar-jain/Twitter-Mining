import enchant
import json
import pandas as pd

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer

# File Path : Change accordingly
filename = "/Users/pratik/Downloads/dataset/review.json"
output_text = []

lemmatizer = WordNetLemmatizer()

# function to read a review and append it to the list
# if it is useful


def filereader(line):
    review_line = json.loads(line)
    if review_line['useful'] > 0:
        out = review_line['text'].replace('\n', '')
        output_text.append(out)


count = 0
with open(filename, 'r') as f:
    for line in f:
        count += 1
        if count < 10000:
            filereader(line)
        else:
            break

tokenizer = RegexpTokenizer(r'\w+')

# package to check if a word is in Dictionary
d = enchant.Dict("en_US")

output_text2 = []
for reviews in output_text:
    filtered_words = []
    for word in tokenizer.tokenize(reviews):
        if d.check(word) and not word.isdigit():
            lemmatizer.lemmatize(word)
            filtered_words.append(word.lower())
    output_text2.append(' '.join(filtered_words))

review_document = [' '.join(output_text2)]

# function to create Bag of Words by removing stop words
vectorizer = CountVectorizer(stop_words='english')
vectorizer.fit_transform(review_document)
names = list(vectorizer.get_feature_names())
count = (vectorizer.transform(review_document).toarray()).tolist()

# creating a dictionary of words in the document and the count of that word
dict_vocab = {}

for i in range(len(names)):
    dict_vocab[names[i]] = count[0][i]

df = pd.DataFrame(list(dict_vocab.items()), columns=['Word', 'Count'])
print(df)
