from sklearn.feature_extraction.text import CountVectorizer
import json
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import random
from nltk.tokenize import sent_tokenize, word_tokenize
from functools import reduce
import numpy as np
from sklearn.feature_selection import SelectFromModel
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest

def get_dataset2():
    dataset = {}
    dataset["data"] = []
    dataset["target"] = []

    handler = open("health.txt", "r")
    list = json.load(handler)
    grades = []
    for pairs in list:
        for grade,text in pairs.items():
            if grade == "MAX":
                grades.append(99999)
            else:
                grades.append(int(grade[0:-1]))
        grades.sort()

        idx = 0
        for grade in grades:
            if grade == 99999:
                gradex = "MAX"
            else:
                gradex = "".join([str(grade), "L"])
            text = "".join([pairs[gradex], " "])

            sents = sent_tokenize(text)
            sent_avg_len = 0
            sent_cnt = 1
            word_avg_len = 0
            word_cnt = 1;
            for sent in sents:
                for word in word_tokenize(sent):
                    word_avg_len += len(word)
                    word_cnt += 1
                sent_avg_len += len(word_tokenize(sent))
                sent_cnt += 1
            sent_avg_len /= sent_cnt
            word_avg_len /= word_cnt
            feature = []
            feature.append(sent_avg_len)
            feature.append(word_avg_len)
            dataset["data"].append(feature)
            dataset["target"].append(idx)

            idx += 1
        grades.clear()
    return dataset

def get_dataset():
    dataset = {}
    dataset["data"] = []
    dataset["target"] = []

    handler = open("health.txt", "r")
    list = json.load(handler)
    grades = []
    for pairs in list:
        for grade,text in pairs.items():
            if grade == "MAX":
                grades.append(99999)
            else:
                grades.append(int(grade[0:-1]))
        grades.sort()

        idx = 0
        for grade in grades:
            if grade == 99999:
                gradex = "MAX"
            else:
                gradex = "".join([str(grade), "L"])
            text = "".join([pairs[gradex], " "])

            loop_idx = idx
            #while loop_idx >= 0:
            dataset["data"].append(text)
            dataset["target"].append(idx)
            # loop_idx -= 1


            idx += 1

        grades.clear()


    return dataset

def get_sample_dataset():
    dataset = {}
    dataset["data"] = []
    dataset["target"] = []

    dataset["data"] = ["a aa", "aa a", "a aaa", "a aaa","a aa", "aa a", "a aaa", "a aaa","a aa", "aa a", "a aaa", "a aaa","c cc","cc  ","c ","cc ","c ","c "]
    dataset["target"] = [1,1,1,1,1,1,1,1,1,1,1,1,3,3,3,3,3,3]

    return dataset


dataset1 = get_dataset()
dataset2 = get_dataset2()

ngrams = [2,3,4,5]
Cs = [1, 10, 100, 1000,10000,100000]
features = [10000,50000,100000,150000,200000,240000]

# samp_order = random.sample(range(len(y)),len(y))
# X = [X[ind] for ind in samp_order]
# y = [y[ind] for ind in samp_order]
for feature in features:
    for ngram in ngrams:
        # word-level
        count_vect = CountVectorizer(min_df=0, max_df=9999, binary=True, lowercase=True, stop_words=None,
                                     ngram_range=(1, ngram))
        X1 = count_vect.fit_transform(dataset1["data"])
        X1 = X1.todense()
        y1 = dataset1["target"]

        # feature-level

        X2 = dataset2["data"]
        y2 = dataset2["target"]

        X = np.append(X1, np.matrix(X2), axis=1)
        # for idx in range(len(y1)):
        #     X[idx] = np.append(X1[idx], np.matrix(X2[idx]), axis=1)
        y = y1
        X = SelectKBest(chi2, k=feature).fit_transform(X, y)

        for c in Cs:
            #clf = LogisticRegression(multi_class='ovr', C=c)
            clf = svm.SVC(C=c, kernel='linear')
            scores = cross_val_score(clf, X, y, cv=10, n_jobs=-1, verbose=0)
            key = " ".join(["feature",str(feature) ,"c", str(c), "ngram", str(ngram)])
            print(key, reduce(lambda x, y: x + y, scores) / len(scores))
