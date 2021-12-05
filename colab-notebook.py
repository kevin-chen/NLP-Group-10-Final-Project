import requests
from bs4 import BeautifulSoup
import pickle
import json
import re

def getBookTexts():
    def get_titles_and_urls(website_list):
        titles = []
        links = []
        for counter, website in enumerate(website_list):
            bookshelfPage = requests.get(
                "https://web.archive.org/web/20200229062920/" + website)
            soup = BeautifulSoup(bookshelfPage.content, "html.parser")
            bookshelfContainer = soup.find("div", class_="mw-parser-output")
            bookList = bookshelfContainer.find_all("li")
            for book in bookList:
                if book.find("img") and book.find("img")["alt"] == "BookIcon.png":
                    bookLink = book.find('a')
                    bookTitle = bookLink.text
                    titles.append(bookTitle)
                    links.append(bookLink["href"])
            print('Website', counter+1, 'information acquired!')
        print('Is length of titles scrapped and links scrapped equal?', len(titles)==len(links))
        return titles, links

    websites = ["https://www.gutenberg.org/wiki/Children%27s_Literature_(Bookshelf)", 
                "https://www.gutenberg.org/wiki/Children%27s_Fiction_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Adventure_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Fantasy_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Humor_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Mystery_Fiction_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Movie_Books_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Science_Fiction_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Children%27s_History_(Bookshelf)",
                "https://www.gutenberg.org/wiki/Plays_(Bookshelf)"]
    titles, links = get_titles_and_urls(websites)

    links_to_search = []
    for x in links:
        links_to_search.append(x.split('/')[-1])
    len(links_to_search)

    special_cases = [57, 158, 189, 189, 590, 941, 2175]
    for x in special_cases:
        titles.pop(x)
        links_to_search.pop(x)

    def parseBookText(to_find):
        bookTextRequest = None
        try:
            bookTextRequest = requests.get("https://www.gutenberg.org/ebooks/" + str(to_find) + ".txt.utf-8")
        except:
            try:
                bookTextRequest = requests.get("https://www.gutenberg.org/files/" + str(to_find) + "/" + str(to_find) + "-0.txt")
            except:
                pass
        if bookTextRequest:
            bookText = BeautifulSoup(bookTextRequest.content, "html.parser").text
            return bookText

    texts = []
    for i in range(0, len(links_to_search)):
        to_find = links_to_search[i]
        print(i, to_find)
        text = parseBookText(to_find)
        texts.append(text)
        print('Text acquired!')

    print(len(texts))
    print(texts)

    with open('bookTitleAndText.data', 'wb') as f:
        pickle.dump([titles, texts], f)

def getLexiles():
    with open('bookTitleAndText.data', 'rb') as f:
        full_text_titles, full_text_texts = pickle.load(f)

    books = []
    authors = []
    lexiles = []

    def getLexileInfo(bookTitle):
        response = requests.post("https://atlas-fab.lexile.com/free/search", data={
            "filters": {
                "language": "english"
            },
            "sort_by": "-score",
            "spanish_br_range_search": False,
            "term": bookTitle,
            "results_per_page": 20,
            "page": 1
        }, headers={
            'accept': 'application/json; version=1.0'
        })
        titles, authors, lexiles = [], [], []
        data = json.loads(response.content)['data']
        results = data['results']
        for result in results:
            try:
                title = result['title']
                author = result['authors'][0]
                lexile = result['measurements']['english']['lexile']
                titles.append(title)
                authors.append(author)
                lexiles.append(lexile)
            except:
                pass
        return titles, authors, lexiles

    for x in range(0, len(full_text_titles)):
        print(x)
        value = str(full_text_titles[x]).replace("/", ' ').replace('!', '')
        print('Finding books')
        print('Finding authors')
        print('Finding levels')
        titles, authors_of_books, levels = getLexileInfo(value)
        books.append(titles)
        authors.append(authors_of_books)
        lexiles.append(levels)

    print(books, authors, lexiles)

    with open('lexile_levels.data', 'wb') as f:
        pickle.dump([books, authors, lexiles], f)

def scrub():
    with open('bookTitleAndText.data', 'rb') as f:
        full_text_titles, full_text_texts = pickle.load(f)
    
    titles_from_text = []
    
    for x in range(0, len(full_text_texts)):
        parse1 = []
        parse2 = []
        parse3 = []
        parse4 = []
        print(full_text_texts[x])
        if full_text_texts[x] == None:
            continue
        parse1.append(re.sub('\n', ' ', full_text_texts[x]))
        print(parse1[0])
        if len(parse1[0].split('THE END'))==2:
            parse2.append(parse1[0].split('THE END')[0])
        elif len(parse1[0].split("End of the Project Gutenberg EBook"))==2:
            parse2.append(parse1[0].split("End of the Project Gutenberg EBook")[0])
        elif len(parse1[0].split('The End'))==2:
            parse2.append(parse1[0].split('The End')[0])
        elif len(parse1[0].split('End of Project Gutenberg\'s'))==2:
            parse2.append(parse1[0].split('End of Project Gutenberg\'s')[0])
        elif len(parse1[0].split('END OF THE PROJECT GUTENBERG EBOOK'))==2:
            parse2.append(parse1[0].split('END OF THE PROJECT GUTENBERG EBOOK')[0]) 
        elif len(parse1[0].split('END OF THIS PROJECT GUTENBERG EBOOK'))==2:
            parse2.append(parse1[0].split('END OF THIS PROJECT GUTENBERG EBOOK')[0])
        elif len(parse1[0].split('The Project Gutenberg Etext'))==4:
            parse2.append(parse1[0].split('The Project Gutenberg Etext')[2])
        elif len(parse1[0].split('*Project Gutenberg Etext'))==4:
            parse2.append(parse1[0].split('*Project Gutenberg Etext')[2])
        elif len(parse1[0].split('End of Project Gutenberg Etext'))==2:
            parse2.append(parse1[0].split('End of Project Gutenberg Etext')[0])
        elif len(parse1[0].split('End of this Project Gutenberg Etext'))==2:
            parse2.append(parse1[0].split('End of this Project Gutenberg Etext')[0])
        elif len(parse1[0].split('End of the Project Gutenberg Etext'))==2:
            parse2.append(parse1[0].split('End of the Project Gutenberg Etext')[0])
        elif len(parse1[0].split('FINIS.'))==2:
            parse2.append(parse1[0].split('FINIS.')[0])
        else:
            print('problem at: ', x)
    #     print('3. removing anything at ebook related at beginning of text')
        if len(parse2[0].split('START OF THIS PROJECT GUTENBERG EBOOK'))==2:
            parse3.append(parse2[0].split('START OF THIS PROJECT GUTENBERG EBOOK')[1])
        elif len(parse2[0].split("START OF THE PROJECT GUTENBERG EBOOK"))==2:
            parse3.append(parse2[0].split("START OF THE PROJECT GUTENBERG EBOOK")[1])
        elif len(parse2[0].split("THIS EBOOK WAS ONE OF PROJECT GUTENBERG'S EARLY FILES PRODUCED AT A TIME WHEN PROOFING METHODS AND TOOLS WERE NOT WELL DEVELOPED."))==2:
            parse3.append(parse2[0].split("THIS EBOOK WAS ONE OF PROJECT GUTENBERG'S EARLY FILES PRODUCED AT A TIME WHEN PROOFING METHODS AND TOOLS WERE NOT WELL DEVELOPED.")[1])
        elif len(parse2[0].split("THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS"))==2:
            parse3.append(parse2[0].split("THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS")[1].split('*END*')[1])
        elif len(parse2[0].split('START OF THE PROJECT GUTENBERG ETEXT'))==2:
            parse3.append(parse2[0].split('START OF THE PROJECT GUTENBERG ETEXT')[1])
        elif len(parse2[0].split('The Project Gutenberg Etext of'))==3:
            parse3.append(parse2[0].split('The Project Gutenberg Etext of')[2])
        else:
            print('problem at: ', x)
        if len(parse3[0].split('***'))==2:
            parse4.append(parse3[0].split('***')[1])
        elif len(parse3[0].split('***'))==48:
            if len(parse3[0].split('***')[47].split('*'))==2:
                parse4.append(parse3[0].split('***')[47].split('*')[1])
            else:
                parse4.append(parse3[0].split('***')[47])
        elif len(parse3[0].split('***'))==3:
            if len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team'))==2:
                parse4.append(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[1])
            elif len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team'))==1:
                if len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)'))==2:
                    parse4.append(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[1])
                elif len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)'))==1:
                    if len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.org'))==2:
                        parse4.append(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.org')[1])
                    elif len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.ac.uk'))==2:
                        parse4.append(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.ac.uk')[1])
                    elif len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.edu/women/.'))==2:
                        parse4.append(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('.edu/women/.')[0])
                    elif len(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('     '))==839:
                        parse4.append(parse3[0].split('***')[1].split('Online Distributed Proofreading Team')[0].split('.zip)')[0].split('This eBook was')[1])
                    else:
                        parse4.append(parse3[0])
                else:
                    print('review: ', x)
            else:
                print('look at: ', x)
        elif len(parse3[0].split('***'))==7:
            parse4.append(parse3[0])
        else:
            print('problem at: ', x)
        print('Book number ', x, ' done!')
        titles_from_text.append(parse3[0].split('*** ')[0].strip().title())
    
    print(len(full_text_texts))
    print(len(titles_from_text))

    with open('lexile_levels.data', 'rb') as f:
        books, authors, lexiles = pickle.load(f)

    search_results_books = []
    for i in range(0, len(books)):
        for j in range(0, len(books[i])):
            if books[i][j] == titles_from_text[i]:
                print(i, j, books[i][j], titles_from_text[i])

scrub()
