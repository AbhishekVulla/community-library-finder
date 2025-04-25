import sqlite3
import os
import pandas as pd
from sample_data import SAMPLE_BOOKS

# Database file
DB_FILE = "library.db"

def get_db_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    """Initialize the database with tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create books table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        age_group TEXT NOT NULL,
        description TEXT,
        cover_url TEXT,
        popularity INTEGER DEFAULT 0
    )
    ''')
    
    # Create suggestions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        genre TEXT NOT NULL,
        age_group TEXT NOT NULL,
        description TEXT,
        cover_url TEXT,
        submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Check if we need to populate the database with sample data
    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]
    
    if book_count == 0:
        # Populate with sample data if database is empty
        for book in SAMPLE_BOOKS:
            cursor.execute('''
            INSERT INTO books (title, author, genre, age_group, description, cover_url, popularity)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                book['title'],
                book['author'],
                book['genre'],
                book['age_group'],
                book['description'],
                book['cover_url'],
                book['popularity']
            ))
    
    conn.commit()
    conn.close()

def get_all_books():
    """Retrieve all books from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books ORDER BY popularity DESC")
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books

def get_books_by_filter(genre=None, age_group=None, search_query=None):
    """Get books filtered by genre, age group, and/or search query"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    
    if genre:
        query += " AND genre = ?"
        params.append(genre)
    
    if age_group:
        query += " AND age_group = ?"
        params.append(age_group)
    
    if search_query:
        query += " AND (title LIKE ? OR author LIKE ?)"
        search_param = f"%{search_query}%"
        params.extend([search_param, search_param])
    
    query += " ORDER BY popularity DESC"
    
    cursor.execute(query, params)
    books = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return books

def get_all_genres():
    """Get all unique genres from the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT genre FROM books ORDER BY genre")
    genres = [row[0] for row in cursor.fetchall()]
    conn.close()
    return genres

def add_book_suggestion(title, author, genre, age_group, description, cover_url):
    """Add a book suggestion to the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO suggestions (title, author, genre, age_group, description, cover_url)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, author, genre, age_group, description, cover_url))
    
    conn.commit()
    conn.close()
    return True
