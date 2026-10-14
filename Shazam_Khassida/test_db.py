import sqlite3
import collections

conn = sqlite3.connect('data/processed/hashes.db')
cursor = conn.cursor()
cursor.execute("SELECT hash, COUNT(*) FROM fingerprints GROUP BY hash ORDER BY COUNT(*) DESC LIMIT 20")
print("Most frequent hashes in DB:")
for r in cursor.fetchall():
    print(r)

cursor.execute("SELECT COUNT(*) FROM fingerprints")
print(f"Total hashes: {cursor.fetchone()[0]}")
