import requests
from bs4 import BeautifulSoup
from datetime import datetime

def transportVicSearch(search, tram=False):
	if tram:
		url = f'https://vic.transportsg.me/tram/tracker/fleet?fleet={search}'
	else:
		url = f'https://vic.transportsg.me/metro/tracker/consist?consist={search}'

	try:
		res = requests.get(url).text

		soup = BeautifulSoup(res, features="lxml")

		elements = soup.find_all('div', class_="trip")

		if not elements:
			return ["Error: No trips found. Train may be invalid or not currently running."]

		trip_texts = [element.text for element in elements]

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

		q.put(days)
	except Exception as e:
		return [f'Error: {e}']
