import lexile_library as lx
import json

bookshelves = ["http://www.gutenberg.org/wiki/Children%27s_Literature_(Bookshelf)"]

bookTitles, bookNums = lx.parseBookshelves(bookshelves)
print("Book Titles:", bookTitles)

bookMap = lx.parseBookText(bookTitles, bookNums)
print("Book Map:", bookMap)

bookTitles, bookNums, lexileScores = lx.getAllLexileScores(bookTitles, bookNums)
print("Lexile Scores:", lexileScores)

# data = lx.generateData(bookTitles, bookNums, lexileScores, bookMap)
# print("Output Data:", data)
# for i in range(12):
#     print("Grade", i, len(data[i]))

# file = open("filtered-data.json", "w")
# json.dump(data, file)
# file.close()
