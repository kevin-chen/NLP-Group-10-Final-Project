import lexile_library as lx
import json
import pickle
import re

def part1():
    bookTitles, bookNums = lx.parseBookshelves()
    print(len(bookTitles), len(bookNums))
    bookTitles, bookNums, bookTexts = lx.parseBookText(bookTitles, bookNums)
    print(len(bookTitles), len(bookNums), len(bookTexts))

    with open('part1.data', 'wb') as f:
        pickle.dump([bookTitles, bookTexts], f)

def part2():
    with open('part1.data', 'rb') as f:
        bookTitles, bookTexts = pickle.load(f)

    foundBookTitles = []
    foundBookAuthors = []
    foundLexileScores = []
    for i in range(len(bookTitles)):
        bookTitle = bookTitles[i]
        lexileInfo = lx.getLexileInfo(bookTitle)
        if lexileInfo != None:
            titles, authors, lexiles = lexileInfo
            foundBookTitles.append(titles)
            foundBookAuthors.append(authors)
            foundLexileScores.append(lexiles)
    
    print(len(foundBookTitles), len(foundBookAuthors), len(foundLexileScores))

    with open('part2.data', 'wb') as f:
        pickle.dump([foundBookTitles, foundBookAuthors, foundLexileScores], f)

def part3():
    with open('part1.data', 'rb') as f:
        bookTitles, _, bookTexts = pickle.load(f)

    parse1 = []
    parse2 = []
    parse3 = []
    parse4 = []
    titles_from_text = []
    for x in range(0, len(bookTexts)):
    #     print('1. removing license agreement at end')
        parse1.append(re.sub('\n', ' ', bookTexts[x]))
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
        print('Book number ', x, ' done!')
        titles_from_text.append(parse3[x].split('*** ')[0].strip().title())

    print(len(bookTexts), len(titles_from_text))

    with open('part3.data', 'wb') as f:
        pickle.dump(titles_from_text, f)

def part4():
    with open('part2.data', 'rb') as f:
        foundBookTitles, foundBookAuthors, foundLexileScores = pickle.load(f)
    
    with open('part3.data', 'rb') as f:
        titles_from_text = pickle.load(f)
        
    # search_results_books = []
    for i in range(0, len(foundBookTitles)):
        for j in range(0, len(foundBookTitles[i])):
            if foundBookTitles[i][j] == titles_from_text[i]:
                print(i, j, foundBookTitles[i][j], titles_from_text[i])
    
    search_results_books = []
    for i, j in enumerate(foundBookTitles):
        try:
            search_results_books.append(j[0])
        except:
            search_results_books.append('')
    print(search_results_books)

    search_results_lexiles = []
    for i, j in enumerate(lexiles):
        try:
            search_results_lexiles.append(j[0])
        except:
            search_results_lexiles.append('')
    print(search_results_lexiles)



def main():
    # part1()
    # part2()
    part3()

if __name__ == "__main__":
    main()