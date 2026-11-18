import sqlite3

def init_db():
    connection = sqlite3.connect("references.db")

    connection.execute("""
        CREATE TABLE IF NOT EXISTS source_references (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER
        )
    """)

    connection.commit()
    connection.close()

