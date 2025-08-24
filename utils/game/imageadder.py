import csv
import sqlite3
import os

from photosubmissions.manager import getUserID


async def acceptGuesserPhoto(id: int, station: str, difficulty: str, mode: str, username: str):
    # read sql db
    id = str(id)
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    c.execute("SELECT * FROM submissions WHERE id = ? ", (id,))
    rows = c.fetchall()
    conn.close()
    
    image_filename = rows[0][2]
    guesserPath = f'assets/guesser/images/'
    imagePath = f'photosubmissions/photos/{image_filename}'
    
    if not os.path.exists(guesserPath):
        os.makedirs(guesserPath)
    
    # move image
    os.rename(imagePath, guesserPath + image_filename)
    
    
    
    print(f'adding to {mode}.csv: {id}, {station}, {difficulty}')
    with open(f'utils/game/images/{mode}.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([f"https://flying-thrush-early.ngrok-free.app/guesser/{image_filename}", station, difficulty, username])
