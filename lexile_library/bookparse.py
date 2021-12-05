import requests
from bs4 import BeautifulSoup

bookshelves = ["http://www.gutenberg.org/wiki/Children%27s_Literature_(Bookshelf)", 
                "http://www.gutenberg.org/wiki/Children%27s_Fiction_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Adventure_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Fantasy_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Humor_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Mystery_Fiction_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Movie_Books_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Science_Fiction_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Children%27s_History_(Bookshelf)",
                "http://www.gutenberg.org/wiki/Plays_(Bookshelf)"]

def parseBookshelves():
    bookTitles = []
    bookNums = []
    for bookshelfLink in bookshelves:
        bookshelfPage = requests.get(
            "https://web.archive.org/web/20200229062920/" + bookshelfLink)
        soup = BeautifulSoup(bookshelfPage.content, "html.parser")
        bookshelfContainer = soup.find("div", class_="mw-parser-output")
        bookList = bookshelfContainer.find_all("li")
        for book in bookList:
            if book.find("img") and book.find("img")["alt"] == "BookIcon.png":
                bookLink = book.find('a')
                bookTitle = bookLink.text
                bookNum = bookLink["href"].split('/')[-1]
                bookTitles.append(bookTitle)
                bookNums.append(bookNum)
    return bookTitles, bookNums


def parseBookText(bookTitles, bookNums):
    foundBookTitles = []
    foundBookNums = []
    foundBookTexts = []
    bookMap = dict()
    for i in range(len(bookNums)):
        bookTitle = bookTitles[i]
        bookNum = bookNums[i]
        bookTextRequest = None
        try:
            bookTextRequest = requests.get("https://www.gutenberg.org/ebooks/" + str(bookNum) + ".txt.utf-8")
        except:
            try:
                bookTextRequest = requests.get("https://www.gutenberg.org/files/" + str(bookNum) + "/" + str(bookNum) + "-0.txt")
            except:
                pass
        if bookTextRequest:
            bookText = BeautifulSoup(bookTextRequest.content, "html.parser").text
            foundBookTitles.append(bookTitle)
            foundBookNums.append(bookNum)
            foundBookTexts.append(bookText)
    return foundBookTitles, foundBookNums, foundBookTexts
