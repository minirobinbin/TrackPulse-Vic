import csv
import requests
import io

def getPhotoCredits(train):
    # image credits:
    url = 'https://railway-photos.xm9g.net/credit.csv'
    search_value = train.upper()

    response = requests.get(url)
    response.raise_for_status() 

    csv_content = response.content.decode('utf-8')
    csv_reader = csv.reader(io.StringIO(csv_content))

    result_value = None
    for row in csv_reader:
        if row[0] == search_value:
            result_value = row[1]
            break
    if result_value == None:
        result_value = "XM9G's Railway Photos"
    return result_value

