import sqlite3

connection = sqlite3.connect("patients.db")

cursor = connection.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS history(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_text TEXT,

    ai_response TEXT
)

""")

connection.commit()

def save_data(user, ai):

    cursor.execute(

        "INSERT INTO history(user_text, ai_response) VALUES(?, ?)",

        (user, ai)
    )

    connection.commit()