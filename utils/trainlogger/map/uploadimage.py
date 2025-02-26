import os
from dotenv import load_dotenv
import requests

def get_imgbb_key():
    load_dotenv()
    imgbb_key = os.getenv('IMGBB')
    
    if not imgbb_key:
        raise ValueError("IMGBB_API_KEY not found in environment variables")
    
    return imgbb_key

def uploadImage(file, name=None):
    imgbb_key = get_imgbb_key()
    url = "https://api.imgbb.com/1/upload"

    files = {
        "image": open(file, "rb")
    }
    params = {
        "key": imgbb_key
    }

    if name:
        params["name"] = name

    response = requests.post(url, files=files, params=params)
    response.raise_for_status()

    return response.json()["data"]["url"]