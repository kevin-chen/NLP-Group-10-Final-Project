# %%
## data_processing.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import time
import pickle
from math import floor
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import StaleElementReferenceException
import re
# from sklearn.manifold import TSNE
import nltk
from nltk.tokenize import TextTilingTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem.snowball import SnowballStemmer
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from sklearn.preprocessing import LabelEncoder
# from keras.utils.np_utils import to_categorical
import random
# from keras import models, layers, optimizers
# from keras.models import load_model

options = Options()
options.add_argument("--headless")

# %% [markdown]
# 
# # Obtain <a id='Obtain'></a>

# %%
def get_titles_and_urls(website_list):

    '''To acquire a list of titles and website extenstions for gutenberg.org from the Bookshelves part of the website. 
    Requires a list of website urls to be passed in. 
    Returns titles and link extensions'''

    titles = []
    links = []
    for counter, website in enumerate(website_list):
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        driver.get(website)
        for x, y in enumerate(driver.find_elements(By.XPATH,"./html/body/div[2]/div[2]/div[1]/ul/li[@class='booklink']")):
            try:
                titles.append(y.find_elements(By.XPATH,'./a/span[2]/span[1]')[0].text)
                links.append(y.find_elements(By.XPATH,'./a')[0].get_attribute('href'))
                
            except:
                continue
        driver.quit()
        print('Website', counter+1, 'information acquired!')
    print('Is length of titles scrapped and links scrapped equal?', len(titles)==len(links))
    return titles, links

websites = ["https://www.gutenberg.org/ebooks/bookshelf/216",   # children's myths
            "https://www.gutenberg.org/ebooks/bookshelf/18",    # children's fiction
            "https://www.gutenberg.org/ebooks/bookshelf/20",    # children's lit
            "https://www.gutenberg.org/ebooks/bookshelf/82",    # adventure
            "https://www.gutenberg.org/ebooks/bookshelf/36",    # fantasy
            "https://www.gutenberg.org/ebooks/bookshelf/44",    # humor
            "https://www.gutenberg.org/ebooks/bookshelf/51",    # mystery fiction   
            "https://www.gutenberg.org/ebooks/bookshelf/49",    # movie books
            "https://www.gutenberg.org/ebooks/bookshelf/19",    # children's history
            "https://www.gutenberg.org/ebooks/bookshelf/59",    # plays
            ]

titles, links = get_titles_and_urls(websites)

links_to_search = []
for x in links:
    links_to_search.append(x.split('/')[4])
len(links_to_search)

# %%
special_cases = {"22980"}

texts = []
urls_used = []
urls_not_used = []
for i in range(0, len(links_to_search)):

    to_find = links_to_search[i]
    print(i, to_find)

    # skip speical cases like audio books
    if to_find in special_cases:
        continue

    try:
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        driver.get("https://www.gutenberg.org/files/"+to_find+"/"+to_find+"-0.txt")
        #driver.get("https://www.gutenberg.org/ebooks/"+to_find+".txt.utf-8")
        text = driver.find_element(By.XPATH,'//pre')
        texts.append(text.text)
        driver.quit()
        urls_used.append(i)
        print('Text acquired!')
    except NoSuchElementException as inst:
        driver.quit()
        print(inst)          # __str__ allows args to be printed directly,
        driver = webdriver.Firefox(options=options)
        driver.implicitly_wait(5)
        # driver.get("https://www.gutenberg.org/files/"+to_find+"/"+to_find+"-0.txt")
        driver.get("https://www.gutenberg.org/cache/epub/"+to_find+"/"+"pg" + to_find + ".txt")
        text = driver.find_element(By.XPATH,'//pre')
        texts.append(text.text)
        driver.quit()
        urls_used.append(i)
        print('Text acquired!')
    #driver.quit()

print(len(texts))
titles.pop(45)

file = open('full_texts.pickle', 'wb')
pickle.dump([titles, texts], file)
file.close()



# %% [markdown]
# ## Lexile

# %%
file = open('full_texts.pickle', 'rb')
full_text_titles, full_text_texts = pickle.load(file)
file.close()

# %%
driver = webdriver.Firefox(options=options)
driver.implicitly_wait(5)
driver.get("https://hub.lexile.com/find-a-book/search")
# choose not to do survey
ask_me_later_button = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div/div[2]/button[1]")
ask_me_later_button.click()

books = []
authors = []
lexiles = []

# for x in range(0, 10):
for x in range(0, len(full_text_titles)):
    print(x)
    value = str(full_text_titles[x]).replace("/", ' ').replace('!', '')
    search_bar = driver.find_element(By.XPATH,'//input[@name="quickSearch"]')
    search_bar.send_keys(value)
    search_button = driver.find_element(By.XPATH,'//button[text()="Search"]')
    search_button.click()
    print('Finding books')
    titles = driver.find_elements(By.XPATH,'//*[@data-testid="book-title"]')
    book_titles = []
    for result in titles:
        book_titles.append(result.text)
    # print(get_xpath_from_element(driver,result))
    print('Finding authors')
    authors_of_books = driver.find_elements(By.XPATH,'//*[@data-testid="book-authors"]')
    book_authors = []
    for result in authors_of_books:
        book_authors.append(result.text)
    print('Finding levels')
    levels = driver.find_elements(By.CLASS_NAME,'sc-erkbxa.kVUyez')
    lexile_levels = []
    for result in levels:
        lexile_levels.append(result.text)
    books.append(book_titles)
    authors.append(book_authors)
    lexiles.append(lexile_levels)
    go_back_button = driver.find_element(By.XPATH,"/html/body/div[2]/div[2]/div[1]/div[2]/div/nav/div[2]/ul/li[1]/a")
    go_back_button.click()
driver.close()

# %%
with open('lexile_levels.pickle', 'wb') as f:
    pickle.dump([books, authors, lexiles], f)

# %% [markdown]
# # Scrub <a id='Scrub'></a>

# %%
with open('full_texts.pickle', 'rb') as file:
    full_text_titles, full_text_texts = pickle.load(file)

# %%
parse1 = []
parse2 = []
parse3 = []
parse4 = []
titles_from_text = []
for x in range(0, len(full_text_texts)):
#     print('1. removing license agreement at end')
    parse1.append(re.sub('\n', ' ', full_text_texts[x]))
#     print('2. removing extras at the end of the text')
    if len(parse1[x].split('THE END'))==2:
        parse2.append(parse1[x].split('THE END')[0])
    elif len(parse1[x].split("End of the Project Gutenberg EBook"))==2:
        parse2.append(parse1[x].split("End of the Project Gutenberg EBook")[0])
    elif len(parse1[x].split('The End'))==2:
        parse2.append(parse1[x].split('The End')[0])
    elif len(parse1[x].split('End of Project Gutenberg\'s'))==2:
        parse2.append(parse1[x].split('End of Project Gutenberg\'s')[0])
    elif len(parse1[x].split('END OF THE PROJECT GUTENBERG EBOOK'))==2:
        parse2.append(parse1[x].split('END OF THE PROJECT GUTENBERG EBOOK')[0]) 
    elif len(parse1[x].split('END OF THIS PROJECT GUTENBERG EBOOK'))==2:
        parse2.append(parse1[x].split('END OF THIS PROJECT GUTENBERG EBOOK')[0])
    elif len(parse1[x].split('The Project Gutenberg Etext'))==4:
        parse2.append(parse1[x].split('The Project Gutenberg Etext')[2])
    elif len(parse1[x].split('*Project Gutenberg Etext'))==4:
        parse2.append(parse1[x].split('*Project Gutenberg Etext')[2])
    elif len(parse1[x].split('End of Project Gutenberg Etext'))==2:
        parse2.append(parse1[x].split('End of Project Gutenberg Etext')[0])
    elif len(parse1[x].split('End of this Project Gutenberg Etext'))==2:
        parse2.append(parse1[x].split('End of this Project Gutenberg Etext')[0])
    elif len(parse1[x].split('End of the Project Gutenberg Etext'))==2:
        parse2.append(parse1[x].split('End of the Project Gutenberg Etext')[0])
    elif len(parse1[x].split('FINIS.'))==2:
        parse2.append(parse1[x].split('FINIS.')[0])
    else:
        print('problem at: ', x)
        # parse2.append(parse1[x]) #chenhe's mod

#     print('3. removing anything at ebook related at beginning of text')
    if len(parse2[x].split('START OF THIS PROJECT GUTENBERG EBOOK'))==2:
        parse3.append(parse2[x].split('START OF THIS PROJECT GUTENBERG EBOOK')[1])
    elif len(parse2[x].split("START OF THE PROJECT GUTENBERG EBOOK"))==2:
        parse3.append(parse2[x].split("START OF THE PROJECT GUTENBERG EBOOK")[1])
    elif len(parse2[x].split("THIS EBOOK WAS ONE OF PROJECT GUTENBERG'S EARLY FILES PRODUCED AT A TIME WHEN PROOFING METHODS AND TOOLS WERE NOT WELL DEVELOPED."))==2:
        parse3.append(parse2[x].split("THIS EBOOK WAS ONE OF PROJECT GUTENBERG'S EARLY FILES PRODUCED AT A TIME WHEN PROOFING METHODS AND TOOLS WERE NOT WELL DEVELOPED.")[1])
    elif len(parse2[x].split("THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS"))==2:
        parse3.append(parse2[x].split("THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS")[1].split('*END*')[1])
    elif len(parse2[x].split('START OF THE PROJECT GUTENBERG ETEXT'))==2:
        parse3.append(parse2[x].split('START OF THE PROJECT GUTENBERG ETEXT')[1])
    elif len(parse2[x].split('The Project Gutenberg Etext of'))==3:
        parse3.append(parse2[x].split('The Project Gutenberg Etext of')[2])
    else:
        print('problem at: ', x)
        # parse3.append(parse2[x]) #chenhe's mod

    if len(parse3[x].split('***'))==2:
        parse4.append(parse3[x].split('***')[1])
    elif len(parse3[x].split('***'))==48:
        if len(parse3[x].split('***')[47].split('*'))==2:
            parse4.append(parse3[x].split('***')[47].split('*')[1])
        else:
            parse4.append(parse3[x].split('***')[47])
    elif len(parse3[x].split('***'))==3:
        if len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team'))==2:
            parse4.append(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[1])
        elif len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team'))==1:
            if len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)'))==2:
                parse4.append(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[1])
            elif len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)'))==1:
                if len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.org'))==2:
                    parse4.append(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.org')[1])
                elif len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.ac.uk'))==2:
                    parse4.append(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.ac.uk')[1])
                elif len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.edu/women/.'))==2:
                    parse4.append(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.edu/women/.')[0])
                elif len(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('     '))==839:
                    parse4.append(parse3[x].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('This eBook was')[1])
                else:
                    parse4.append(parse3[x])
            else:
                print('review: ', x)
        else:
            print('look at: ', x)
    elif len(parse3[x].split('***'))==7:
        parse4.append(parse3[x])
    else:
        print('problem at: ', x)
        # parse4.append(parse3[x]) #chenhe's mod
        
    print('Book number ', x, ' done!')
    titles_from_text.append(parse3[x].split('*** ')[0].strip().title())

# %%
with open('lexile_levels.pickle', 'rb') as file:
    books, authors, lexiles = pickle.load(file)

# %%
search_results_books = []
for i in range(0, len(books)):
    for j in range(0, len(books[i])):
        if books[i][j] == titles_from_text[i]:
            print(i, j, books[i][j], titles_from_text[i])
#             if j == 0: then append books[i][j] to search_results_books
#             if the above hasn't been done yet, then append books[i][j] to search_results_books
# use break

# %%
search_results_books = []
for i, j in enumerate(books):
    try:
        search_results_books.append(j[0])
    except:
        search_results_books.append('')
search_results_books

# %%
search_results_lexiles = []
for i, j in enumerate(lexiles):
    try:
        search_results_lexiles.append(j[0])
    except:
        search_results_lexiles.append('')
search_results_lexiles

# %%
length_lexiles = []
for x in search_results_lexiles:
    length_lexiles.append(x!='')
print('Number of scraped texts with associated lexile results: ', sum(length_lexiles))

# %%
for i in range(0, len(search_results_books)):
    search_results_books[i] = re.sub('\n', ' ', search_results_books[i]).title()
search_results_books[:5]

# %%
labeled_data = pd.DataFrame()
labeled_lexiles = []
labeled_titles = []
labeled_text = []
for x in range(0, len(search_results_lexiles)):
    title_from_search = str(search_results_books[x]).lower().strip()
    title_from_full = str(full_text_titles[x]).lower().strip()
    if  (title_from_search == title_from_full) or (title_from_full in title_from_search):
        labeled_lexiles.append(search_results_lexiles[x])
        labeled_titles.append(full_text_titles[x])
        labeled_text.append(full_text_texts[x])
    # else:
        # print(x, 'No title or lexile match to scrapped material')

labeled_data['Lexiles'] = labeled_lexiles
labeled_data['Titles'] = labeled_titles
labeled_data['Texts'] = labeled_text
# print('Number of scraped texts that can be labeled with lexile levels: ', len(labeled_data))
labeled_data.sample(5)


# %%
with open("Lexiles.txt", 'w') as f:
    for i in  labeled_data['Lexiles']:
        f.write(i + "\n")
        

# %%
print('total labeled titles: ',len(set(labeled_data['Titles'])))

# %%
# nans identification
print(len(labeled_data))
labeled_data.isna().sum()

# %%
print('duplicated rows: ' + str(labeled_data.duplicated().sum()))

# %%
labeled_data = labeled_data.reset_index().drop('index', axis=1)

# %%
print('total labeled titles: ',len(set(labeled_data['Titles'])))

# %%
labeled_data = labeled_data.drop_duplicates("Titles")
labeled_data = labeled_data[labeled_data["Lexiles"] != "NP"]
labeled_data = labeled_data = labeled_data.reset_index().drop('index', axis=1)
labeled_data

# %%
print('total labeled titles: ',len(set(labeled_data['Titles'])))

# %%
with open('labeled_data.pickle', 'wb') as file:
    pickle.dump(labeled_data, file)


