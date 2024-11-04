import sqlite3
import pandas as pd

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('creditcard_fraud.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        Time REAL,
        V1 REAL,
        V2 REAL,
        V3 REAL,
        V4 REAL,
        V5 REAL,
        V6 REAL,
        V7 REAL,
        V8 REAL,
        V9 REAL,
        V10 REAL,
        V11 REAL,
        V12 REAL,
        V13 REAL,
        V14 REAL,
        V15 REAL,
        V16 REAL,
        V17 REAL,
        V18 REAL,
        V19 REAL,
        V20 REAL,
        V21 REAL,
        V22 REAL,
        V23 REAL,
        V24 REAL,
        V25 REAL,
        V26 REAL,
        V27 REAL,
        V28 REAL,
        Amount REAL,
        Class INTEGER
    )
''')

# Commit the changes
conn.commit()

# Load the data from creditcard.csv
data = pd.read_csv('creditcard.csv')

# Insert the data into the transactions table
data.to_sql('transactions', conn, if_exists='replace', index=False)

# Fetch and display some records to confirm
cursor.execute("SELECT * FROM transactions LIMIT 5")
rows = cursor.fetchall()
for row in rows:
    print(row)

# Commit and close the connection
conn.commit()
conn.close()
