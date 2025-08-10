import sqlite3

async def addSubmission(photo, userid, date, location, photofor, number=None):
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS submissions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, display_id INTEGER, photo text, userid text, date text, location text, photofor text, number text)''')
    # Get next display_id
    c.execute("SELECT COUNT(*) FROM submissions")
    next_display_id = c.fetchone()[0] + 1
    c.execute("INSERT INTO submissions (display_id, photo, userid, date, location, photofor, number) VALUES (?, ?, ?, ?, ?, ?, ?)", 
              (next_display_id, photo, userid, date, location, photofor, number))
    conn.commit()
    submission_id = c.lastrowid
    conn.close()
    return submission_id, next_display_id

async def removeSubmission(submission_id):
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    # Get userid before deleting
    c.execute("SELECT userid FROM submissions WHERE id = ?", (submission_id,))
    result = c.fetchone()
    userid = result[0] if result else None

    c.execute("DELETE FROM submissions WHERE id = ?", (submission_id,))
    conn.commit()

    # Reassign display_id values
    c.execute("SELECT id FROM submissions ORDER BY display_id")
    rows = c.fetchall()
    for new_display_id, (row_id,) in enumerate(rows, start=1):
        c.execute("UPDATE submissions SET display_id = ? WHERE id = ?", (new_display_id, row_id))
    conn.commit()
    conn.close()
    return userid

async def getUserID(submission_id):
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    c.execute("SELECT userid FROM submissions WHERE id = ?", (submission_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

async def returnQueue(user=None):
    conn = sqlite3.connect('photosubmissions/db.db')
    c = conn.cursor()
    if user:
        c.execute("SELECT * FROM submissions WHERE userid = ? ORDER BY display_id", (user,))
    else:
        c.execute("SELECT * FROM submissions ORDER BY display_id")
    rows = c.fetchall()
    conn.close()
    return rows