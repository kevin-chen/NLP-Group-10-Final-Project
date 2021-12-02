from nltk.corpus import words, gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from random import sample

# n = 10
bunchofwords = "hello my name is bob and this is a sentence about something"
# print(gutenberg.words(bunchofwords))

# START OF THIS PROJECT GUTENBERG EBOOK


# rand_words = ' '.join(sample(bunchofwords.words(), n))
# print(rand_words)

stopWords = set(stopwords.words('english'))
words = word_tokenize(bunchofwords)
wordsFiltered = []

for w in words:
    if w not in stopWords:
        wordsFiltered.append(w)

print(wordsFiltered)

# str = "HELLOEND OF THE PROJECT GUTENBERG EBOOK"
# print(str.find("END OF THE PROJECT GUTENBERG EBOOK"))