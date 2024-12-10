import requests
from bs4 import BeautifulSoup
from datetime import datetime

from bs4 import BeautifulSoup
import requests

def transportVicSearch(search, tram=False):
    if tram:
        url = f'https://transportvic.me/tram/tracker/fleet?fleet={search}'
    else:
        url = f'https://transportvic.me/metro/tracker/consist?consist={search}'

    try:
        res = requests.get(url).text

        soup = BeautifulSoup(res, features="lxml")

        # Find all divs with class "trip" but not "trip inactive"
        elements = soup.find_all('div', class_='trip')
        active_elements = [e for e in elements if 'inactive' not in e.get('class', [])]

        if not active_elements:
            return ["Error: No active trips found. Train may be invalid or not currently running."]

        trip_texts = [element.text for element in active_elements]

        return trip_texts
    except Exception as e:
        return [f'Error: {e}']


def TRAMtransportVicSearch(search, tram=True):
	return transportVicSearch(search, tram=tram)

def montagueDays(q):
	url = f'https://howmanydayssincemontaguestreetbridgehasbeenhit.com/static/js/main.4728b675.chunk.js'

	try:
		res = requests.get(url).text

		days = (datetime.now() - datetime.strptime(res.split('date":"')[1].split('"')[0], "%Y-%m-%d")).days

		q.put(str(days))
	except Exception as e:
		return [f'Error: {e}']
