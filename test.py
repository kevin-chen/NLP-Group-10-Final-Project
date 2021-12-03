import lexile_library as lx

bookTitles = ["Flower Fables", "Eight cousins"]
bookNums = [1,2]

bookTitles, bookNums, lexileScores = lx.getAllLexileScores(bookTitles, bookNums)
print("Output:", bookTitles, bookNums, lexileScores)