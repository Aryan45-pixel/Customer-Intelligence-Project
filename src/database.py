import sqlite3
import hashlib

# ---------------- DATABASE CONNECTION ----------------
conn = sqlite3.connect('customer.db', check_same_thread=False)
cursor = conn.cursor()

# ======================================================
# 🔐 USER TABLE (AUTH SYSTEM)
# ======================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
""")

# ======================================================
# 📊 CUSTOMER TABLE (UPDATED WITH USERNAME)
# ======================================================
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    age INTEGER,
    frequency INTEGER,
    purchase REAL,
    segment TEXT,
    high_spender INTEGER,
    churn INTEGER
)
""")

conn.commit()

# ======================================================
# 🔐 AUTH FUNCTIONS
# ======================================================

# ---------------- HASH PASSWORD ----------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- CREATE USER ----------------
def create_user(username, password):
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# ---------------- LOGIN USER ----------------
def login_user(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return cursor.fetchone()


# ======================================================
# 📊 CUSTOMER DATA FUNCTIONS (UPDATED)
# ======================================================

# ---------------- INSERT DATA (UPDATED) ----------------
def insert_data(username, age, frequency, purchase, segment, high_spender, churn):
    try:
        cursor.execute("""
            INSERT INTO customers (username, age, frequency, purchase, segment, high_spender, churn)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (username, age, frequency, purchase, segment, high_spender, churn))

        conn.commit()
    except Exception as e:
        print(f"Insert Error: {e}")


# ---------------- FETCH USER DATA (UPDATED) ----------------
def fetch_data(username):
    cursor.execute(
        "SELECT * FROM customers WHERE username=?",
        (username,)
    )
    return cursor.fetchall()


# ---------------- FETCH ALL DATA (OPTIONAL ADMIN) ----------------
def fetch_all_data():
    cursor.execute("SELECT * FROM customers")
    return cursor.fetchall()