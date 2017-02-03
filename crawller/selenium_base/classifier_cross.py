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
import os

num_cpus = multiprocessing.cpu_count()

handler = open("news3.txt", "r")
obj = json.load(handler)

data_text_x = {}
data_stat_x = {}
data_y = {}

if os.path.exists("data_text_x"):
    f_data_text_x = open("data_text_x", "rb")
    f_data_stat_x = open("data_stat_x", "rb")
    f_data_y = open("f_data_y", "rb")
    data_text_x = pickle.load(f_data_text_x)
    data_stat_x = pickle.load(f_data_stat_x)
    data_y = pickle.load(f_data_y)
else:
    for category in obj:
        category_clean = category.strip()
        if category_clean not in data_text_x:
            print(category_clean)
            data_text_x[category_clean] = []
            data_stat_x[category_clean] = []
            data_y[category_clean] = []

        data_entries = obj[category]
        for data_entry in data_entries:
            for label in data_entry:
                text = data_entry[label]

                data_text_x[category_clean].append(text)
                data_y[category_clean].append(int(label))

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

                data_stat_x[category_clean].append([word_avg_len, sent_avg_len])

    f_data_text_x = open("data_text_x", "wb")
    f_data_stat_x = open("data_stat_x", "wb")
    f_data_y = open("f_data_y", "wb")
    pickle.dump(data_text_x, f_data_text_x)
    pickle.dump(data_stat_x, f_data_stat_x)
    pickle.dump(data_y, f_data_y)

for origin_category in data_text_x:
    for target_category in data_text_x:

        count_vect = CountVectorizer(min_df=0, max_df=9999, binary=True, lowercase=True, stop_words=None,
                                     ngram_range=(1, 5))
        y = data_y[origin_category]

        x_text = count_vect.fit_transform(data_text_x[origin_category])
        x_text = SelectKBest(chi2, k=5000).fit_transform(x_text, y)

        x_stat = data_stat_x[origin_category]

        x = np.concatenate((x_text.todense(), np.matrix(x_stat)), axis=1)



        # regression model
        reg = linear_model.Ridge(alpha = 1.0)
        reg.fit(x, y)

        y2 = data_y[target_category]

        x_text2 = count_vect.fit_transform(data_text_x[target_category])
        x_text2 = SelectKBest(chi2, k=5000).fit_transform(x_text2, y2)
        x_stat2 = data_stat_x[target_category]
        x2 = np.concatenate((x_text2.todense(), np.matrix(x_stat2)), axis=1)

        r_square = reg.score(x2, y2)

        print(origin_category, target_category, str(r_square))



