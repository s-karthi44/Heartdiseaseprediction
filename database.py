import sqlite3

# Connect Database
conn = sqlite3.connect("heart.db", check_same_thread=False)
cursor = conn.cursor()

# -----------------------------
# Users Table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# -----------------------------
# Prediction History Table
# -----------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    prediction TEXT,
    probability REAL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()


# -----------------------------
# Register User
# -----------------------------
def register_user(fullname, email, username, password):
    try:
        cursor.execute("""
        INSERT INTO users(fullname,email,username,password)
        VALUES(?,?,?,?)
        """, (fullname, email, username, password))

        conn.commit()
        return True

    except:
        return False


# -----------------------------
# Login User
# -----------------------------
def login_user(username, password):

    cursor.execute("""
    SELECT * FROM users
    WHERE username=? AND password=?
    """, (username, password))

    return cursor.fetchone()


# -----------------------------
# Save Prediction
# -----------------------------
def save_prediction(username, prediction, probability):

    cursor.execute("""
    INSERT INTO predictions(username,prediction,probability)
    VALUES(?,?,?)
    """, (username, prediction, probability))

    conn.commit()


# -----------------------------
# Get Prediction History
# -----------------------------
def get_history(username):

    cursor.execute("""
    SELECT prediction,probability,date
    FROM predictions
    WHERE username=?
    ORDER BY date DESC
    """, (username,))

    return cursor.fetchall()