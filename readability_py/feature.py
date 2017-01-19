from nltk.corpus import cmudict
from nltk import word_tokenize, sent_tokenize

class word:
    def __init__(self, word):
        self.word = word
        self.d = cmudict.dict()

    def __init__(self, word, d):
        self.word = word
        self.d = d

    def num_syl(self):
        try:
            items = [len(list(y for y in x if y[-1].isdigit())) for x in self.d[self.word.lower()]]
            return items[0]
        except:
            return 0


class text:
    def __init__(self, text):
        self.text = text
        self.d = cmudict.dict()

    def num_words(self):
        return len([token for token in word_tokenize(self.text)])

    def spw(self):
        tokens = word_tokenize(self.text)

        syls = 0
        for token in tokens:
            syls += word(token, self.d).num_syl()

        spw = syls / len(tokens)
        return spw

        # while True:
        #     cnt += 1
        #
        #     s = cnt * 100
        #     e = (cnt+1) * 100
        #     if (cnt+1)*100 > len(self.text)-1 :
        #         e = len(self.text)-1
        #
        #     syls = 0
        #     for wd in tokens[s, e]:
        #         syls += word(wd, self.d).num_syl()
        #
    def sl(self):
        lens = 0
        sents = sent_tokenize(self.text)
        for sent in sents:
            lens += len(word_tokenize(sent))
        sl = lens / len(sents)
        return sl

    def wl(self):
        return self.spw()*100

    def lw(self):
        tokens = word_tokenize(self.text)
        lw = 0
        for token in tokens:
            if word(token, self.d).num_syl() >= 3:
                lw += 1
        return lw


if __name__ == '__main__':
    # wd = word("appled")
    # print(wd.num_syl())

    tx = text("i am monkey.")
    print(tx.num_words())


