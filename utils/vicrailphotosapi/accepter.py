import os
import sqlite3
from PIL import Image

from utils.vicrailphotosapi.vrfAPI import upload_image



def acceptPhoto(id, username, trainType, featured:bool, note, number, location, date):
    id = str(id)
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions WHERE id = ? ", (id,))
    rows = c.fetchall()
    conn.close()
    if len(rows) == 0:
        return 'No submission found with that ID'
    elif rows[0][6] not in ['both', 'website']:
        return 'This submission is not for the website'
    
    else:
        if number == None:
            number = rows[0][7]
        if location == None:
            location = rows[0][5]
        if date == None:
            date = rows[0][4]
        
        image_filename = rows[0][2]
        image_extension = os.path.splitext(image_filename)[1].lower()
        webp_filename = os.path.splitext(image_filename)[0] + '.webp'

        # Convert the image to WebP
        convertToWEBP(
            input_path=f'photosubmissions/photos/{image_filename}',
            output_path=f'photosubmissions/photos/{webp_filename}'
        )

        print(f'Uploading photo for {username} with number {number}, type {trainType}, location {location}, date {date}, featured: {featured}, note: {note}')
        url = upload_image(
            image_path=f'photosubmissions/photos/{webp_filename}',
            number=number,
            train_type=trainType,
            location=location,
            date=date,
            photographer=username,
            featured='Y' if featured else 'N',
            note=note
        )

        if 'error' in url:
            return f'Error uploading photo: {url["error"]}'
        else:
            return 'Photo accepted and uploaded successfully'
    
def convertToWEBP(input_path, output_path, quality=100):

    try:
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file {input_path} does not exist.")
        
        img = Image.open(input_path)
        
        # Convert to RGB if the image is in RGBA
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img.save(output_path, 'WEBP', quality=quality)
        print(f"Image successfully converted to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        