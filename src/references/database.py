
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


def add_reference(title, author, year):
    """Tallentaa uuden lähteen tietokantaan."""
    connection = sqlite3.connect("references.db")

    connection.execute(
        """
        INSERT INTO source_references (title, author, year)
        VALUES (?, ?, ?)
        """,
        (title, author, year)
    )

    connection.commit()
    connection.close()


def get_references():
    """Hakee kaikki tallennetut lähteet."""
    connection = sqlite3.connect("references.db")

    references = connection.execute(
        "SELECT * FROM source_references"
    ).fetchall()

    connection.close()
    return references


def delete_reference(reference_id):
    """Poistaa lähteen tunnisteen perusteella."""
    connection = sqlite3.connect("references.db")

    connection.execute(
        "DELETE FROM source_references WHERE id = ?",
        (reference_id,)
    )

    connection.commit()
    connection.close()
