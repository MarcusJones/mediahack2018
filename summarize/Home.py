from collections import defaultdict
from string import punctuation
from heapq import nlargest



import string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

file=open('data.txt','rU')
str=file.read()
translator = str.maketrans('', '', string.punctuation)
print('==================================================================')
print(str)
text=str.translate(translator)
print('==================================================================')

print(text)
print('==================================================================')

words = word_tokenize(text)

freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue
    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1

print(freqTable)

sentences = sent_tokenize(text)
#print(sentences[:10])
sentenceValue = dict()

#***************************************************************************************
'''
for sentence in sentences:
    for wordValue in freqTable:
        if wordValue[0] in sentence.lower():
            if sentence[:12] in sentenceValue:
                sentenceValue[sentence[:2]] += wordValue[1]
            else:
                sentenceValue[sentence[:2]] = wordValue[1]



sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# Average value of a sentence from original text
average = int(sumValues/ len(sentenceValue))


summary = ''
for sentence in sentences:
        if sentence[:12] in sentenceValue and sentenceValue[sentence[:12]] > (1.5 * average):
            summary +=  " " + sentence


print(summary)
'''

#=========================================================================================================









class FrequencySummarizer:
    def __init__(self, min_cut=0.1, max_cut=0.9):
        """
         Initilize the text summarizer.
         Words that have a frequency term lower than min_cut
         or higer than max_cut will be ignored.
        """
        self._min_cut = min_cut
        self._max_cut = max_cut
        self._stopwords = set(stopwords.words('english') + list(punctuation))

    def _compute_frequencies(self, word_sent):
        """
          Compute the frequency of each of word.
          Input:
           word_sent, a list of sentences already tokenized.
          Output:
           freq, a dictionary where freq[w] is the frequency of w.
        """
        freq = defaultdict(int)
        for s in word_sent:
            for word in s:
                if word not in self._stopwords:
                    freq[word] += 1
        # frequencies normalization and fitering
        m = float(max(freq.values()))
        for w in freq.keys():
            freq[w] = freq[w] / m
            if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
                del freq[w]
        return freq

    def summarize(self, text, n):
        """
          Return a list of n sentences
          which represent the summary of text.
        """
        sents = sent_tokenize(text)
        assert n <= len(sents)
        word_sent = [word_tokenize(s.lower()) for s in sents]
        self._freq = self._compute_frequencies(word_sent)
        ranking = defaultdict(int)
        for i, sent in enumerate(word_sent):
            for w in sent:
                if w in self._freq:
                    ranking[i] += self._freq[w]
        sents_idx = self._rank(ranking, n)
        return [sents[j] for j in sents_idx]

    def _rank(self, ranking, n):
        """ return the first n sentences with highest ranking """
        return nlargest(n, ranking, key=ranking.get)


def main():
    print("Hello World!")


if __name__ == "__main__":
    fs = FrequencySummarizer()
    fs.summarize(text,2)










