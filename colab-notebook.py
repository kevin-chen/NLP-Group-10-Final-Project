import requests
from bs4 import BeautifulSoup
import pickle
import json

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
    if data['total_results'] == 0:
        return [], [], []
    for result in results:
        title = result['title']
        author = result['authors'][0]
        lexile = result['measurements']['english']['lexile']
        titles.append(title)
        authors.append(author)
        lexiles.append(lexile)
    return titles, authors, lexiles

for x in range(0, len(full_text_titles)):
    print(x)
    value = str(full_text_titles[x]).replace("/", ' ').replace('!', '')
    titles, authors_of_books, levels = getLexileInfo(value)
    print('Finding books')
    book_titles = []
    for result in titles:
        book_titles.append(result.text)
    print('Finding authors')
    book_authors = []
    for result in authors_of_books:
        book_authors.append(result.text)
    print('Finding levels')
    lexile_levels = []
    for result in levels:
        lexile_levels.append(result.text)
    books.append(book_titles)
    authors.append(book_authors)
    lexiles.append(lexile_levels)

with open('lexile_levels.data', 'wb') as f:
    pickle.dump([books, authors, lexiles], f)