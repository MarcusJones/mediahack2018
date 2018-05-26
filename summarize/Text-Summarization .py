from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import PorterStemmer
import string
from string import punctuation


ps = PorterStemmer()
stemmer = SnowballStemmer('english')
stopWords = set(stopwords.words('english'))
file_name=input("file name= ")
file = open(file_name, 'r')

text=file.read()



words = word_tokenize(text)

freqTable = dict()
for word in words:
    word = word.lower()
    if word in stopWords:
        continue

    word = stemmer.stem(word)

    if word in freqTable:
        freqTable[word] += 1
    else:
        freqTable[word] = 1
sentences = sent_tokenize(text)
sentenceValue = dict()

for sentence in sentences:
    for word, freq in freqTable.items():
        if word in sentence.lower():
            if sentence in sentenceValue:
                sentenceValue[sentence] += freq
            else:
                sentenceValue[sentence] = freq
        
        
sumValues = 0
for sentence in sentenceValue:
    sumValues += sentenceValue[sentence]

# Average value of a sentence from original text
average = int(sumValues / len(sentenceValue))

summary = ""
for sentence in sentences:
    if len(words)>500:
        if sentence in sentenceValue and sentenceValue[sentence] > (1.5 * average):
            summary += " " + sentence
    else:
        if sentence in sentenceValue and sentenceValue[sentence] > (1.3 * average):
            summary += " " + sentence
        

# print(summary)
f = open('output.txt','w')
f.write(summary)

###################################

w=""
words = summary.split()
for word in words:
    if not word in stopWords:
        word  = ps.stem(word)
        w+=" "+word
        
print("=====================  text summarization with stemming  =====================")
print(w)
print("\n")

###################################

f.close()
file.close()
print("=====================  text summarization without stemming  =====================")
print(summary)
