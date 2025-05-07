import sqlite3

import sqlite3

DB_NAME = "votes.db"

def connect():
    return sqlite3.connect(DB_NAME)

def setup_db():
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
        voter_id TEXT UNIQUE NOT NULL,
        FOREIGN KEY(candidate_id) REFERENCES candidates(id)
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS voters (
        id TEXT PRIMARY KEY
    )
    """)

    conn.commit()
    conn.close()

def add_candidate(name):
    """
    function allows user to add candidates to vote menu
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO candidates (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def get_candidates():
    """
    will retrieve data from database
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM candidates")
    candidates = cur.fetchall()
    conn.close()
    return candidates

def has_voted(voter_id):
    """
    this checks to see if the ID has already been used or not 
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM voters WHERE id = ?", (voter_id,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def register_voter(voter_id):
    """
    takes and saves voter's ID 
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO voters (id) VALUES (?)", (voter_id,))
    conn.commit()
    conn.close()

def record_vote(candidate_id, voter_id):
    """
    saves voter's vote into a database
    """
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO votes (candidate_id, voter_id) VALUES (?, ?)", (candidate_id, voter_id))
    conn.commit()
    conn.close()

def count_votes():
    """
    Counts the votes
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
