import requests

# THIS IS DIFFRNT TO THE ONE USED IN THE TRAIN PHOTO COMMAND!
# THIS ONE ONLY RETURNS THE FIRST IMAGE AND ALSO REQUIRS CORRECT FORMATTING!!
def getImage(number):
    photo_url = f"https://railway-photos.xm9g.net/photos/{number}.webp"

    # Make a HEAD request to check if the photo exists
    URLresponse = requests.head(photo_url)
    if URLresponse.status_code == 200:
        return(photo_url)
    else:
        return(None)
    
    
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

# get VICSIG URL
def vicSigURL(carriageNumber, trainType):
    if trainType == 'VLocity':
        url = f'https://vicsig.net/passenger/railmotor/{carriageNumber}/VLocity'
    elif trainType == 'Sprinter':
        url = f'https://vicsig.net/passenger/railmotor/{carriageNumber}/Sprinter'
    elif trainType == 'N Class':
        url = f'https://vicsig.net/index.php?page=locomotives&number={carriageNumber}&class=N&type=Diesel-Electric&orgstate=V'
        
    else:
        if trainType in ['HCMT', "X'Trapolis 2.0"]:
            url = ''
        
        
        
        if trainType == "X'Trapolis 100":
            name = 'X%27Trapolis'
        elif trainType == "EDI Comeng" or trainType == "Alstom Comeng":
            name = 'Comeng'
        elif trainType == 'Siemens Nexas':
            name = 'Siemens'
        elif trainType == 'HCMT':
            name = 'HCMT'
            
        if carriageNumber.endswith('M'):
            carType = 'M'
        elif carriageNumber.endswith('T'):
            carType = 'T'
        
            
        url = f'https://vicsig.net/index.php?page=suburban&carriage={carriageNumber}&cartype={carType}&traintype={name}'
    
    return(url)