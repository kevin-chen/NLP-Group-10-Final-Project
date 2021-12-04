import nltk
nltk.download('stopwords')
nltk.download('punkt')

from nltk.corpus import words, gutenberg
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from random import sample
import string

porter = PorterStemmer()

def findGradeLevel(lexileScore):
    if 0 <= lexileScore <= 230:
        return 0
    elif 231 <= lexileScore <= 530:
        return 1
    elif 531 <= lexileScore <= 650:
        return 2
    elif 651 <= lexileScore <= 820:
        return 3
    elif 821 <= lexileScore <= 940:
        return 4
    elif 941 <= lexileScore <= 1010:
        return 5
    elif 1011 <= lexileScore <= 1070:
        return 6
    elif 1071 <= lexileScore <= 1120:
        return 7
    elif 1121 <= lexileScore <= 1185:
        return 8
    elif 1186 <= lexileScore <= 1260:
        return 9
    elif 1261 <= lexileScore <= 1335:
        return 10
    elif 1336 <= lexileScore <= 1385:
        return 11
    else:
        return None


def getFilteredText(bookTitle, bookText):
    startThisPhrase = "START OF THIS PROJECT GUTENBERG EBOOK"
    endThisPhrase = "END OF THIS PROJECT GUTENBERG EBOOK"

    startThisIndex = bookText.find(startThisPhrase)
    endThisIndex = bookText.find(endThisPhrase)

    startThePhrase = "START OF THE PROJECT GUTENBERG EBOOK"
    endThePhrase = "END OF THE PROJECT GUTENBERG EBOOK"

    startTheIndex = bookText.find(startThePhrase)
    endTheIndex = bookText.find(endThePhrase)

    if startThisIndex != -1 and endThisIndex != -1:
        print("Clear This")
        return bookText[startThisIndex + len(startThisPhrase) : endThisIndex]
    elif startTheIndex != -1 and endTheIndex != -1:
        print("Clear The")
        return bookText[startTheIndex + len(startThePhrase) : endTheIndex]
    else:
        print("Start, End This Index:", startThisIndex, endThisIndex)
        print("Start, End The Index:", startTheIndex, endTheIndex)
        print("Phrase within text, Book Title:", bookTitle)
        # print(bookText[:1500])
        return ""


def getSampleFilterWords(stopWords, bookText):
    startPhrase = "START OF THIS PROJECT GUTENBERG EBOOK"
    endPhrase = "END OF THE PROJECT GUTENBERG EBOOK"
    startIndex = bookText.find(startPhrase)
    endIndex = bookText.find(endPhrase)

    if startIndex != -1 and endIndex != -1:
        words = word_tokenize(bookText[startIndex + len(startPhrase) : endIndex])
    else:
        words = word_tokenize(bookText)

    # removes attached punctutations from words
    table = str.maketrans('', '', string.punctuation)
    stripped = [word.translate(table) for word in words]

    wordsFiltered = []
    for word in stripped:
        if word not in stopWords and word.isalpha():
            wordsFiltered.append(porter.stem(word.lower().strip()))

    wordsFiltered = [word.lower().strip() for word in stripped if word not in stopWords and word.isalpha()]
    if len(wordsFiltered) <= 100: return wordsFiltered
    return ' '.join(sample(wordsFiltered, 100))


def generateData(bookTitles, bookNums, bookTexts, lexileScores):
    output = dict()
    stopWords = set(stopwords.words('english'))
    
    for i in range(len(bookNums)):
        entry = dict()
        bookTitle = bookTitles[i]
        bookNum = bookNums[i]
        bookText = bookTexts[i]

        lexileScore = lexileScores[i]
        grade = findGradeLevel(lexileScore)
        filteredText = getFilteredText(bookTitle, bookText)
        
        if filteredText == "":
            continue
        
        entry["title"] = bookTitle
        entry["lexile"] = lexileScore
        entry["words"] = filteredText
        
        if output.get(grade, None) == None:
            output[grade] = [entry]
        else:
            output[grade].append(entry)
        
    return output
