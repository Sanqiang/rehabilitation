from nltk.translate import AlignedSent
from nltk.translate import IBMModel1
import json
from nltk.tokenize import sent_tokenize, word_tokenize

def getSentPair():
    corpus = []
    handler = open("news.txt", "r")
    list = json.load(handler)
    for pairs in list:
        if len(pairs) == 0:
            continue
        min_grade = 12
        max_grade = -1
        temp = {}
        for grade, text in pairs.items():
            grade = int(grade)
            min_grade = min(min_grade, grade)
            max_grade = max(max_grade, grade)
            temp[grade] = text
        text_max = sent_tokenize(temp[max_grade])
        text_min = sent_tokenize(temp[min_grade])
        if len(text_max) != len(text_min):
            x = 1

getSentPair()



