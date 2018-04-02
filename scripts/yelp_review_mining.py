import json
from sklearn.feature_extraction.text import CountVectorizer

# File Path : Change accordingly
filename = "D:/Rishabh/Study/NCSU Classes/SE/review.json"
output_text = []


# function to read a review and append it to the list
def filereader(line):
    gdfJson = json.loads(line)
    out = gdfJson['text'].replace('\n', '')
    output_text.append(out)


with open(filename, 'r') as f:
    for line in f:
        filereader(line)

vectorizer = CountVectorizer()
print( vectorizer.fit_transform(output_text).todense() )
print( vectorizer.vocabulary_ )