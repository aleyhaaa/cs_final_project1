import sqlite3

DB_NAME = "votes.db"

def connect():
    """
    Establish a connection to the SQLite database
    """
    return sqlite3.connect(DB_NAME)

def setup_db():
    """
    Create the candidates and votes tables if they do not exist
    """
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS votes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_id INTEGER NOT NULL,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id)
    )
    """)

    conn.commit()
    conn.close()

def add_candidate(name):
    """
    Insert a new candidate with the given name into the database
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_candidates():
    """
    Retrieve all candidates from the database.
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM candidates")
    candidates = cur.fetchall()
    conn.close()
    return candidates

def record_vote(candidate_id):
    """
    Record a vote for the specified candidate using their unique candidate ID
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO votes (candidate_id) VALUES (?)", (candidate_id,))
    conn.commit()
    conn.close()

def count_votes():
    """
    Count the number of votes each candidate has received and return the results
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT c.name, COUNT(v.candidate_id) as total_votes
        FROM candidates c
        LEFT JOIN votes v ON c.id = v.candidate_id
        GROUP BY c.name
        ORDER BY total_votes DESC
    """)
    results = cur.fetchall()
    conn.close()
    return results
