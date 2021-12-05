import requests
import json

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
    try:
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
    except:
        return None
