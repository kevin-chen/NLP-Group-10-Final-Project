from os import X_OK
import requests
from collections import defaultdict
import math
import json
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

#this block of code gets some data about the data
def dataAboutData(data):
    grades = ["0","1","2","3","4","5","6","7","8","9","10","11"]
    num_of_books_per_grade = []
    avg_num_of_chars_or_words_in_books_per_grade = []
    for grade in grades:
        num_of_books_per_grade.append(len(data[grade]))
        words_in_grade = 0 #This will store the total number words for the grade that is teh current iteration
        for i in range(len(data[grade])):
            words_in_grade += len(data[grade][i]["words"])
        avg_num_of_chars_or_words_in_books_per_grade.append(words_in_grade//len(data[grade]))
    print("num_of_books_per_grade:")
    print( num_of_books_per_grade)
    print("avg_num_of_chars_or_words_in_books_per_grade:")
    print( avg_num_of_chars_or_words_in_books_per_grade)

# api-endpoint
URL1 = "https://raw.githubusercontent.com/kevin-chen/NLP-Group-10-Final-Project/main/regular-data.json"
# sending get request and saving the response as response object
r1 = requests.get(url = URL1)
# extracting data in json format
data1 = r1.json()
f = open('../one-large-text.json')
data2 = json.load(f)

# dataAboutData(data1)
# dataAboutData(data2)
print("When splicing a book for 1000 characters it becomes about this many words:")
print("Grade 2: " + str(len(data2["1"][0]["words"][10000:11000].split())))
print("Grade 7: " + str(len(data2["6"][0]["words"][10000:11000].split())))
print("Grade 12: " + str(len(data2["11"][0]["words"][10000:11000].split())))

closed_class_stop_words = ['a','the','an','and','or','but','about','above','after','along','amid','among',\

                           'as','at','by','for','from','in','into','like','minus','near','of','off','on',\

                           'onto','out','over','past','per','plus','since','till','to','under','until','up',\

                           'via','vs','with','that','can','cannot','could','may','might','must',\

                           'need','ought','shall','should','will','would','have','had','has','having','be',\

                           'is','am','are','was','were','being','been','get','gets','got','gotten',\

                           'getting','seem','seeming','seems','seemed',\

                           'enough', 'both', 'all', 'your' 'those', 'this', 'these', \

                           'their', 'the', 'that', 'some', 'our', 'no', 'neither', 'my',\

                           'its', 'his' 'her', 'every', 'either', 'each', 'any', 'another',\

                           'an', 'a', 'just', 'mere', 'such', 'merely' 'right', 'no', 'not',\

                           'only', 'sheer', 'even', 'especially', 'namely', 'as', 'more',\

                           'most', 'less' 'least', 'so', 'enough', 'too', 'pretty', 'quite',\

                           'rather', 'somewhat', 'sufficiently' 'same', 'different', 'such',\

                           'when', 'why', 'where', 'how', 'what', 'who', 'whom', 'which',\

                           'whether', 'why', 'whose', 'if', 'anybody', 'anyone', 'anyplace', \

                           'anything', 'anytime' 'anywhere', 'everybody', 'everyday',\

                           'everyone', 'everyplace', 'everything' 'everywhere', 'whatever',\

                           'whenever', 'whereever', 'whichever', 'whoever', 'whomever' 'he',\

                           'him', 'his', 'her', 'she', 'it', 'they', 'them', 'its', 'their','theirs',\

                           'you','your','yours','me','my','mine','I','we','us','much','and/or'

                           ]

closed_class_stop_words = set(closed_class_stop_words)



#This block of code will make an array of 12 dicts, each dict has the term freq for a grade level
term_freq_per_grade = [] 
grades = ["0","1","2","3","4","5","6","7","8","9","10","11"]
for grade in grades:
    curr_grade_tf_dict = defaultdict(int)
    for book in data1[grade]: #iterating through array of books
        for word in book["words"]:
            curr_grade_tf_dict[word] += 1
    term_freq_per_grade.append(curr_grade_tf_dict)

TFIDF_vectors = [] #12-long-list. Each element is a dict/TFIDF vector
count = 0
for term_freq_dict in term_freq_per_grade:
    count += 1
    curr_grade_TFIDF_vector = defaultdict(int)
    for word in term_freq_dict:
        num_of_docs_containing = 0
        for term_freq_dict in term_freq_per_grade:
            if word in term_freq_dict:
                num_of_docs_containing +=1
        curr_grade_TFIDF_vector[word] = term_freq_dict[word] * math.log(12/num_of_docs_containing)
    TFIDF_vectors.append(curr_grade_TFIDF_vector)

# print(TFIDF_vectors[0])
grades = ["0","1","2","3","4","5","6","7","8","9","10","11"]
average_sentence_length_per_grade = []
for grade in grades:
    running_length_of_sentences = 0
    num_of_sentences = 0
    for book in data2[grade]:
        sample_from_a_book = book["words"][10000:11000]
        # UNCOMMENT TO SEE THE SAMPLES TAKEN FROM BOOKS
        if grade == "0":
            print(sample_from_a_book)
            print(book["title"])
            print(book["lexile"])
            print("~~~~~~~~~~~~~~~~~~~")
        if type(sample_from_a_book) == str:
            x = sent_tokenize(sample_from_a_book)
            
            if len(x) != 1: #avoid table of contents
                for i in range(1,len(x)-1): #going through sentences
                    sentence_length = len(x[i].split())
                    if sentence_length != 1: # should i include this condition? 
                        # print(grade + ": "+  str(sentence_length))
                        running_length_of_sentences += sentence_length
                        num_of_sentences +=1
    average_sentence_length_per_grade.append(running_length_of_sentences//num_of_sentences)
print(average_sentence_length_per_grade)
        #BUGGY SENTENCE LENGTH COUNTER
        # sample_from_a_book = sample_from_a_book.split()
        # i = 0
        # #Move i to point to a start of a sentence
        # while i< len(sample_from_a_book) and sample_from_a_book[i][-1] not in "?.!":
        #     i+=1
        # i+=1
        # count = 0
        # while i< len(sample_from_a_book):
        #     if sample_from_a_book[i][-1] not in "?.!":
        #         count +=1
        #     else:
        #         print(count)
        #         running_length_of_sentences+= (count +1)
        #         num_of_sentences+=1  
        #         count = 0
        #     i+=1

