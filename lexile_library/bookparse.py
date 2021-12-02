import requests
from bs4 import BeautifulSoup


def parseBookshelves(bookshelves):
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
    # foundBookTitles = []
    # foundBookTexts = []
    bookMap = dict()
    for i in range(len(bookNums)):
        bookTitle = bookTitles[i]
        bookNum = bookNums[i]
        bookTextRequest = None
        try:
            bookTextRequest = requests.get("https://www.gutenberg.org/ebooks/" + str(bookNum) + ".txt.utf-8")
        except:
            pass
        try:
            bookTextRequest = requests.get("https://www.gutenberg.org/files/" + str(bookNum) + "/" + str(bookNum) + "-0.txt")
        except:
            pass
        if bookTextRequest:
            bookText = BeautifulSoup(bookTextRequest.content, "html.parser").text
            bookMap[bookNum] = bookText
            # foundBookTitles.append(bookTitle)
            # foundBookTexts.append(bookText)
    return bookMap
