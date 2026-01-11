import sqlite3
import os

db_path = "data/smart_pm.db"
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Try adding status column
    try:
        cursor.execute("ALTER TABLE backlog_items ADD COLUMN status VARCHAR DEFAULT 'To Do'")
        print("Added status column to backlog_items")
    except sqlite3.OperationalError:
        print("status column already exists or table doesn't exist")

    # Try adding priority column
    try:
        cursor.execute("ALTER TABLE backlog_items ADD COLUMN priority VARCHAR DEFAULT 'Medium'")
        print("Added priority column to backlog_items")
    except sqlite3.OperationalError:
        print("priority column already exists")
    
    conn.commit()
    conn.close()
    print("Migration complete!")
else:
    print("Database not found, nothing to migrate.")
