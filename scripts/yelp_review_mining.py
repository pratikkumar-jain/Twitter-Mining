import enchant
import json
import numpy as np
import os
import pandas as pd
import pdb
import pickle

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer


def filter_documents(docs):
    # package to check if a word is in Dictionary
    english_dict = enchant.Dict("en_US")
    tokenizer = RegexpTokenizer(r'\w+')
    lemmatizer = WordNetLemmatizer()

    output_text2 = []
    filtered_vocab = []
    for reviews in docs:
        filtered_words = []
        for word in tokenizer.tokenize(reviews):
            if english_dict.check(word) and not word.isdigit():
                lemmatizer.lemmatize(word)
                filtered_words.append(word.lower())
        filtered_vocab.extend(filtered_words)
        output_text2.append(' '.join(filtered_words))

    # Slightly optimized function to get filtered vocab. Do not delete.
    # new_filtered_vocab = []
    # for word in tokenizer.tokenize(' '.join(output_text)):
    #         if d.check(word) and not word.isdigit():
    #             lemmatizer.lemmatize(word)
    #             new_filtered_vocab.append(word.lower())

    print("Words filtered!")
    return [' '.join(output_text2)]


def generate_document(filename, max_reviews=50000, savepath=None):

    review_doc = []
    output_text = []

    def filereader(line):
        review_line = json.loads(line)
        # Only take 'useful' reviews
        if review_line['useful'] > 0:
            out = review_line['text'].replace('\n', '')
            output_text.append(out)

    if not os.path.exists('completed_lines.pickle'):
        completed = 0
    else:
        with open('completed_lines.pickle', 'rb') as fp:
            completed = pickle.load(fp)

    count = 0
    with open(filename, 'r') as f:
        for i, line in enumerate(f):
            if i > completed:
                count += 1
                # print(i)
                if count < max_reviews:
                    filereader(line)
                else:
                    break

    completed += count
    print('Reviews Read: {}'.format(completed))
    with open('completed_lines.pickle', 'wb') as fp:
        pickle.dump(completed, fp)

    print("File read!")
    return output_text

    # TODO: Save filtered documents


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

    if not os.path.exists('saved_bag_of_words.pickle'):
        # print("Not Present")
        dict_vocab = {}
    else:
        with open('saved_bag_of_words.pickle', 'rb') as fp:
            dict_vocab = pickle.load(fp)
    # print(dict_vocab)

    for i in range(len(names)):
        if names[i] in dict_vocab:
            dict_vocab[names[i]] += count[0][i]
        else:
            dict_vocab[names[i]] = count[0][i]
    # print(dict_vocab)

    with open('saved_bag_of_words.pickle', 'wb') as fp:
        pickle.dump(dict_vocab, fp)

    df = pd.DataFrame(list(dict_vocab.items()), columns=['word', 'count'])

    # Normalize count
    max_count = df['count'].max()
    min_count = df['count'].min()
    df['normalized_count'] = (df['count'] - min_count) / \
        (max_count - min_count)

    bag_of_words = df.loc[df['normalized_count'] >= 0.1]
    # print(bag_of_words)
    print("bag_of_words created!")
    return bag_of_words


def main():
    file_name = "/Users/pratik/Downloads/dataset/review.json"
    reviews = generate_document(file_name, max_reviews=10)
    filtered_documents = filter_documents(reviews)
    bag_of_review_words = create_bag_of_words(filtered_documents)
    bag_of_review_words.to_pickle("yelp_bag_of_review_words.pkl")


if __name__ == '__main__':
    main()
