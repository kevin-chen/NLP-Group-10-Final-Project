import requests
import json

def getLexileScore(bookTitle):
  response = requests.post("https://atlas-fab.lexile.com/free/search", data={
      "filters": {
          "language": "english"
      },
      "sort_by": "-score",
      "spanish_br_range_search": False,
      "term": bookTitle,
      "results_per_page": 1,
      "page": 1
  }, headers={
    'accept': 'application/json; version=1.0'
  })
  try:
    data = json.loads(response.content)['data']
    # print(data)
    if data['total_results'] == 0 or data['results'][0]['measurements']['english']['lexile_code'] != "" or bookTitle.lower() != data['results'][0]['title'].lower():
      # print("Bad Result", data)
      return None
    else:
      return data['results'][0]['measurements']['english']['lexile']
  except KeyError:
    # print(data)
    return None
  except:
    return None

def getAllLexileScores(bookTitles, bookNums):
  foundBookTitles = []
  foundBookNums = []
  foundLexileScores = []
  for i in range(len(bookTitles)):
    bookTitle = bookTitles[i]
    bookNum = bookNums[i]
    lexileScore = getLexileScore(bookTitle)
    if lexileScore != None:
      foundBookTitles.append(bookTitle)
      foundBookNums.append(bookNum)
      foundLexileScores.append(lexileScore)
  return foundBookTitles, foundBookNums, foundLexileScores