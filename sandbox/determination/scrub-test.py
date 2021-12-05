import requests
from bs4 import BeautifulSoup
import re

endOfText = ['THE END', 'End of the Project Gutenberg EBook', 'The End', 'End of Project Gutenberg\'s', 'END OF THE PROJECT GUTENBERG EBOOK', 'END OF THIS PROJECT GUTENBERG EBOOK', 'The Project Gutenberg Etext', '*Project Gutenberg Etext', 'End of Project Gutenberg Etext', 'End of this Project Gutenberg Etext',  'End of the Project Gutenberg Etext', 'FINIS.']
begOfText = ['START OF THIS PROJECT GUTENBERG EBOOK', 'START OF THE PROJECT GUTENBERG EBOOK', 'THIS EBOOK WAS ONE OF PROJECT GUTENBERG\'S EARLY FILES PRODUCED AT A TIME WHEN PROOFING METHODS AND TOOLS WERE NOT WELL DEVELOPED.', 'THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS', 'START OF THE PROJECT GUTENBERG ETEXT', 'The Project Gutenberg Etext of']

def scrubEnding(text):
    for factor in endOfText:
        if factor == 'The Project Gutenberg Etext' and text.split(factor) == 4:
            return text.split(factor)[2]
        elif factor == '*Project Gutenberg Etext' and text.split(factor) == 4:
            return text.split(factor)[2]
        elif text.split(factor) == 2:
            return text.split(factor)[0]
    return "Ending issue with: " + text

def scrubBeginning(text):
    for factor in begOfText:
        if factor == 'THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS' and text.split(factor) == 2:
            return text.split(factor)[1].split('*END*')[1]
        elif factor == 'The Project Gutenberg Etext of' and text.split(factor) == 3:
            return text.split('The Project Gutenberg Etext of')[2]
        elif text.split(factor) == 2:
            return text.split(factor)[1]
    return "Beginning issue with: " + text

bookTextRequest = requests.get("https://www.gutenberg.org/ebooks/" + str(2726) + ".txt.utf-8")
bookText = BeautifulSoup(bookTextRequest.content, "html.parser").text
# print(bookText)

## TRY TO FIND END OF TEXT
cleanedText = re.sub('\r\n', ' ', bookText)
# print(parse1)
# print(len(parse1[0].split('THE END')))
scrubbed = scrubBeginning(scrubEnding(cleanedText))
print(len(scrubbed))