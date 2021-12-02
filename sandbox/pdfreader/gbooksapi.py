import requests
import json

# Sample API urls
# https://www.google.com/books/feeds/volumes/?q=ISBN%3C9798557824989%3E
# https://www.googleapis.com/books/v1/volumes?q=isbn%3D9798557824989
# https://www.googleapis.com/books/v1/volumes?q=subject:fiction
# https://www.googleapis.com/books/v1/volumes?q=isbn:9798557824989

# Sample isbn
# 9798557824989
# 

isbn = "9798557824989" # https://www.amazon.com/Giraffe-Who-Found-Its-Spots/dp/B08MSQT62R/ref=sr_1_5?keywords=childrens+book&qid=1637179428&sr=8-5
url = 'https://www.googleapis.com/books/v1/volumes?q=isbn:' + isbn
resp = requests.get(url)

parsed = resp.json()
print(json.dumps(parsed, indent=4, sort_keys=True))
print(parsed['items'][0]['volumeInfo']['pageCount'])