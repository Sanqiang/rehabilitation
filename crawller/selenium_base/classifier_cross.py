import json
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
import numpy as np
from sklearn import linear_model
from joblib import Parallel, delayed
import multiprocessing
import pickle

num_cpus = multiprocessing.cpu_count()

handler = open("news3.txt", "r")
obj = json.load(handler)

data_text_x = {}
data_stat_x = {}
data_y = {}

for category in obj:
    if category not in data_text_x:
        print(category)
        data_text_x[category] = []
        data_stat_x[category] = []
        data_y[category] = []

    data_entries = obj[category]
    for data_entry in data_entries:
        for label in data_entry:
            text = data_entry[label]

            data_text_x[category].append(text)
            data_y[category].append(int(label))

            sent_avg_len = 0
            sent_cnt = 1
            word_avg_len = 0
            word_cnt = 1
            sents = sent_tokenize(text)
            for sent in sents:
                sent_avg_len += len(word_tokenize(sent))
                sent_cnt += 1
                for word in word_tokenize(sent):
                    word_avg_len += len(word)
                    word_cnt += 1
            sent_avg_len /= sent_cnt
            word_avg_len /= word_cnt

            data_stat_x[category].append([word_avg_len, sent_avg_len])

pickle.dump(data_text_x, "data_text_x")
pickle.dump(data_stat_x, "data_stat_x")
pickle.dump(data_y, "data_y")

for origin_category in data_text_x:
    for target_category in data_text_x:

        count_vect = CountVectorizer(min_df=0, max_df=9999, binary=True, lowercase=True, stop_words=None,
                                     ngram_range=(1, 5))
        x_text = count_vect.fit_transform(data_text_x[origin_category])
        x_text = SelectKBest(chi2, k=5000).fit_transform(x_text, y)

        x_stat = data_stat_x[origin_category]

        x = np.concatenate((x_text, np.matrix(x_stat)), axis=1)

        y = data_y[origin_category]

        # regression model
        reg = linear_model.Ridge (alpha = 1.0)
        reg.fit(x, y)

        x_text2 = count_vect.fit_transform(data_text_x[target_category])
        x_stat2 = data_stat_x[target_category]
        x2 = np.concatenate((x_text2, np.matrix(x_stat2)), axis=1)
        y2 = data_y[target_category]

        r_square = reg.score(x2, y2)

        print(origin_category, target_category, str(r_square))



