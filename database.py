import sqlite3

DATABASE = "integrity.db"

def get_connection():
    return sqlite3.connect(DATABASE)

def create_database():
    connection = get_connection()
    cursor = connection.cursor()
    # Main registered files
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            original_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Verification history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER NOT NULL,
            current_hash TEXT NOT NULL,
            status TEXT NOT NULL,
            risk_level TEXT NOT NULL,
            hash_difference REAL NOT NULL,
            execution_time REAL NOT NULL,
            checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (file_id) REFERENCES files(id)
        )
    """)
    connection.commit()
    connection.close()


def find_file(filename):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, original_hash
        FROM files
        WHERE filename = ?
        ORDER BY id DESC
        LIMIT 1
    """, (filename,))
    result = cursor.fetchone()
    connection.close()
    return result

def register_file(filename, file_hash):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO files (filename, original_hash)
        VALUES (?, ?)
    """, (filename, file_hash))
    file_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return file_id

def save_history(
    file_id,
    current_hash,
    status,
    risk_level,
    hash_difference,
    execution_time
):

    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO file_history
        (
            file_id,
            current_hash,
            status,
            risk_level,
            hash_difference,
            execution_time
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        file_id,
        current_hash,
        status,
        risk_level,
        hash_difference,
        execution_time
    ))
    connection.commit()
    connection.close()

def get_history():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT
            files.filename,
            file_history.current_hash,
            file_history.status,
            file_history.risk_level,
            file_history.hash_difference,
            file_history.execution_time,
            file_history.checked_at
        FROM file_history
        JOIN files
        ON file_history.file_id = files.id
        ORDER BY file_history.id DESC
    """)

    results = cursor.fetchall()
    connection.close()
    return results