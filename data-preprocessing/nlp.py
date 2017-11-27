# import nltk
import json
import numpy as np
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from data_preprocessing import read_csv
import sys
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.feature_extraction.text import CountVectorizer

stop_words = set(stopwords.words("english"))
print stop_words

ps = PorterStemmer()
vectorizer = CountVectorizer()

reload(sys)
sys.setdefaultencoding('utf8')

# nltk.download()

df_stock_news = read_csv('../assets/article_stock/nytimes1.csv', ',')

def create_corpus(df):
    corpus = []

    news_titles = df['title']
    news_description = df['description']

    for i, title in news_titles.iteritems():
        words = word_tokenize(title)
        stemmed_title = []

        for word in words:
            if word not in stop_words:
                formatted_word = word.decode('utf-8').replace(u"\u2018", "").replace(u"\u2019", "").replace(u"\u201d", "").lower()
                stemmed_word = ps.stem(formatted_word)

                stemmed_title.append(stemmed_word)

                if stemmed_word not in corpus:
                    corpus.append(stemmed_word)

        df.set_value(i, 'title', stemmed_title)

    for i, description in news_description.iteritems():
        words = word_tokenize(description)
        stemmed_description = []

        for word in words:
            if word not in stop_words:
                formatted_word = format_word(word)
                stemmed_word = ps.stem(formatted_word)

                stemmed_description.append(stemmed_word)

                if stemmed_word not in corpus:
                    corpus.append(stemmed_word)

        df.set_value(i, 'description', stemmed_description)

    return corpus

def read_corpus_from_txt():
    with open("corpus.txt", "r") as f:
        read_corpus = json.load(f)
        print "read_corpus"
        print read_corpus
    return read_corpus

def write_corpus_to_txt(corpus):
    with open("corpus.txt", "w") as f:
        return json.dump(corpus, f)

def format_word(word):
    return word.decode('utf-8')\
               .replace(u"\u2018", "")\
               .replace(u"\u2019", "")\
               .replace(u"\u201c", "")\
               .replace(u"\u201d", "")\
               .lower()

corpus = create_corpus(df_stock_news)
# print corpus
# write_corpus_to_txt(corpus)

# corpus = read_corpus_from_txt()

# label_encoder = LabelEncoder()

# encoded_corpus = label_encoder.fit_transform(corpus)

# print "encoded_corpus"
# print encoded_corpus

# corpus = read_corpus_from_txt()



# print bag_of_words

# print 'bag_of_words'
# print bag_of_words

bag_of_words = vectorizer.fit_transform(corpus)
bag_of_words = bag_of_words.toarray()
vocab = vectorizer.get_feature_names()

print 'appl', vectorizer.vocabulary_.get("basketbal")
print "vocab getme apple"
print vocab[vocab.index("basketbal")]

print df_stock_news.columns[3]

zeros = []
for w in vocab:
    zeros.append(0)

df_training_data = pd.DataFrame(0, index=np.arange(df_stock_news.shape[0]), columns=vocab)
# df_training_data.to_csv('zeros.csv')

for i, row in df_stock_news.iterrows():
    title = df_stock_news.loc[i, 'title']
    title = title
    for word in title:
        # print ps.stem(format_word(word))
        if word in vocab:
            print word
            df_training_data.set_value(i, word, df_training_data.loc[i, word] + 1)

for i, row in df_stock_news.iterrows():
    description = df_stock_news.loc[i, 'description']
    description = description
    for word in description:
        # print ps.stem(format_word(word))
        if word in vocab:
            print word
            df_training_data.set_value(i, word, df_training_data.loc[i, word] + 1)

print df_training_data

df_training_data.to_csv('training_data.csv')

# For each, print the vocabulary word and the number of times it
# appears in the training set
# for tag, count in zip(vocab, dist):
#     print count, tag


# onehotencoder = OneHotEncoder(categorical_features=[0, 1])
# df_stock_news = onehotencoder.fit_transform(df_stock_news).toarray()

print df_stock_news.head()