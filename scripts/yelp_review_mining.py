import enchant
import json
import pandas as pd
import numpy as np
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pdb

def generate_document(filename, max_reviews = 50000, savepath = None):
    lemmatizer = WordNetLemmatizer()


    review_doc = []
    output_text = []

    def filereader(line):
        review_line = json.loads(line)
        # Only take 'useful' reviews
        if review_line['useful'] > 0:
            out = review_line['text'].replace('\n', '')
            output_text.append(out)

    count = 0
    with open(filename, 'r') as f:
        for line in f:
            count += 1
            if count < max_reviews:
                filereader(line)
            else:
                break

    print("File read!")

    tokenizer = RegexpTokenizer(r'\w+')

    # package to check if a word is in Dictionary
    english_dict = enchant.Dict("en_US")

    output_text2 = []
    filtered_vocab = []
    for reviews in output_text:
        filtered_words = []
        for word in tokenizer.tokenize(reviews):
            if english_dict.check(word) and not word.isdigit():
                lemmatizer.lemmatize(word)
                filtered_words.append(word.lower())
        filtered_vocab.extend(filtered_words)
        output_text2.append(' '.join(filtered_words))

    ## Slightly optimized function to get filtered vocab. Do not delete.
    # new_filtered_vocab = []
    # for word in tokenizer.tokenize(' '.join(output_text)):
    #         if d.check(word) and not word.isdigit():
    #             lemmatizer.lemmatize(word)
    #             new_filtered_vocab.append(word.lower())

    print("Words filtered!")

    # Filtered review documents
    review_document = [' '.join(output_text2)]

    return output_text2
    # Save here

def create_bag_of_words(documents):

    # function to create Bag of Words by removing stop words
    # We should not use tf-idf, only count
    # vectorizer = TfidfVectorizer(min_df=5, max_df = 0.8, sublinear_tf=True, use_idf =True, stop_words = 'english')
    # train_corpus_tf_idf = vectorizer.fit_transform(documents)
    # test_corpus_tf_idf = vectorizer.transform(X_test)

    vectorizer = CountVectorizer(stop_words='english')
    train_corpus = vectorizer.fit_transform(documents)
    names = list(vectorizer.get_feature_names())
    count = (train_corpus.toarray()).tolist()

    # feature_array = np.array(vectorizer.get_feature_names())
    # tfidf_sorting = np.argsort(train_corpus_tf_idf.toarray()).flatten()[::-1]

    # n = 50
    # top_n = feature_array[tfidf_sorting][:n]
    # print("top: ", top_n)
    # creating a dictionary of words in the document and the count of that word
    dict_vocab = {}

    for i in range(len(names)):
        dict_vocab[names[i]] = count[0][i]

    df = pd.DataFrame(list(dict_vocab.items()), columns=['word', 'count'])

    # Normalize count
    max_count = df['count'].max()
    min_count = df['count'].min()
    df['normalized_count'] = (df['count'] - min_count) / (max_count - min_count)

    bag_of_words = df.loc[df['normalized_count'] >= 0.1]
    print(bag_of_words)

    return bag_of_words

if __name__ == '__main__':
    file_name = "/Users/nirav/workspaces/Twitter-Mining/dataset/review.json"
    filtered_document = generate_document(file_name, max_reviews = 10000)
    create_bag_of_words(filtered_document)
