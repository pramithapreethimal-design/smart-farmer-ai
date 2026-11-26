
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "chat_history.db"


def initialize_database():

    with sqlite3.connect(DB_NAME) as connection:

        cursor = connection.cursor()

        # Check whether messages table exists
        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='messages'
        """)

        table_exists = cursor.fetchone()

        if not table_exists:

            # Create new table with farmer_id
            cursor.execute("""
                CREATE TABLE messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    farmer_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL
                )
            """)

        else:

            # Check existing columns
            cursor.execute("PRAGMA table_info(messages)")

            columns = [
                column[1]
                for column in cursor.fetchall()
            ]

            # Add farmer_id if missing
            if "farmer_id" not in columns:

                cursor.execute("""
                    ALTER TABLE messages
                    ADD COLUMN farmer_id TEXT
                """)

                # Assign old messages to demo farmer
                cursor.execute("""
                    UPDATE messages
                    SET farmer_id = 'farmer_001'
                    WHERE farmer_id IS NULL
                """)


def save_message(farmer_id, role, content):

    with sqlite3.connect(DB_NAME) as connection:

        connection.execute(
            """
            INSERT INTO messages
            (farmer_id, role, content)
            VALUES (?, ?, ?)
            """,
            (farmer_id, role, content)
        )


def get_chat_history(farmer_id):

    with sqlite3.connect(DB_NAME) as connection:

        cursor = connection.execute(
            """
            SELECT role, content
            FROM messages
            WHERE farmer_id = ?
            ORDER BY id
            """,
            (farmer_id,)
        )

        return cursor.fetchall()
