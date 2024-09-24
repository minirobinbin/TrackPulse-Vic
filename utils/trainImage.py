import requests

# THIS IS DIFFRNT TO THE ONE USED IN THE TRAIN PHOTO COMMAND!
# THIS ONE ONLY RETURNS THE FIRST IMAGE AND ALSO REQUIRS CORRECT FORMATTING!!
def getImage(number):
    photo_url = f"https://railway-photos.xm9g.net/photos/{number}.jpg"

    # Make a HEAD request to check if the photo exists
    URLresponse = requests.head(photo_url)
    if URLresponse.status_code == 200:
        return(photo_url)
    
def getTramImage(number):
    photo_url = f"https://railway-photos.xm9g.net/trams/photos/{number}.jpg"

    # Make a HEAD request to check if the photo exists
    URLresponse = requests.head(photo_url)
    if URLresponse.status_code == 200:
        return(photo_url)


def getIcon(type):
    cleaned_type = type.replace(' ', '-').replace("'", '')
    url = f"https://xm9g.net/discord-bot-assets/MPTB/{cleaned_type}.png"
    return(url)

def getStationImage(station):
    type = station.title()
    cleaned_type = type.replace(' ', '%20')
    url = f"https://railway-photos.xm9g.net/stations/photos/{cleaned_type}.jpg"
    URLresponse = requests.head(url)
    if URLresponse.status_code == 200:
        return(url)

    return(None)
