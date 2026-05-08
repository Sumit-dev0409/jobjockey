import sqlite3, os

# Find the database
db_file = None
for name in ['jobjockey.db', 'db.sqlite3']:
    if os.path.exists(name):
        db_file = name
        break

if not db_file:
    print("ERROR: No database found!")
    exit()

print(f"Found database: {db_file}")
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Fix all missing columns
fixes = [
    ("notifications", "seen_by", "TEXT", "[]"),
    ("candidates", "state", "TEXT", ""),
    ("candidates", "college", "TEXT", ""),
    ("candidates", "edu_domain", "TEXT", ""),
    ("candidates", "duration", "TEXT", ""),
    ("reports", "file_data", "TEXT", ""),
    ("meetings", "members", "TEXT", "[]"),
    ("tasks", "deadline", "TEXT", "TBD"),
    ("tasks", "project", "TEXT", ""),
]

for table, col, typ, default in fixes:
    try:
        existing = [r[1] for r in c.execute(f'PRAGMA table_info({table})').fetchall()]
        if col not in existing:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ} DEFAULT '{default}'")
            conn.commit()
            print(f"FIXED: {table}.{col}")
        else:
            print(f"OK: {table}.{col}")
    except Exception as e:
        print(f"Error on {table}.{col}: {e}")

conn.close()
print("\nDone! Now restart: uvicorn main:app --reload")
