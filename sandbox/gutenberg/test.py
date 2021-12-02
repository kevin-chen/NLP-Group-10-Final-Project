import lexile_library as lx
import json
# from bs4 import BeautifulSoup
# import requests

# bookTextRequest = requests.get("https://www.gutenberg.org/ebooks/22234.txt.utf-8")
# print(BeautifulSoup(bookTextRequest.content, "html.parser").text)

# bookshelves = ["http://www.gutenberg.org/wiki/Children%27s_Literature_(Bookshelf)"]

# bookTitles, bookNums = lx.parseBookshelves(bookshelves)
# # print("Book Titles:", bookTitles)
# # print("Book Titles:", bookNums)

# bookMap = lx.parseBookText(bookTitles, bookNums)
# # print("Book Text:", bookMap)

# bookTitles, bookNums, lexileScores = lx.getAllLexileScores(bookTitles, bookNums)
# # print(lexileScores)
# # print(bookNums)



# data = lx.generateData(bookTitles, bookNums, lexileScores, bookMap)
# print("THE F-ING DATA", data)
# file = open("sample.json", "w")
# json.dump(data, file)
# file.close()


bookTitles = ["Flower Fables", "EightCousins"]

# lexileScore = lx.getLexileScore("Eight Cousins")
# print("Lexile Scores:", lexileScore)

allScores = lx.getAllLexileScores(bookTitles, [1,2])
print(allScores)

# print(lx.generateData(["HelloWorld", "Book1"], [1, 2], [100, 300], {
#     1: "This is a book about, HelloWorld",
#     2: "This is something"
# }))