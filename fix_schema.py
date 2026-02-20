import sqlite3
import os

# Path to the database
params = {
    'db_path': os.path.join('instance', 'blockchain.db')
}

def fix_schema():
    if not os.path.exists(params['db_path']):
        print(f"Database not found at {params['db_path']}")
        return

    conn = sqlite3.connect(params['db_path'])
    cursor = conn.cursor()

    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(admin)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'school_name' not in columns:
            print("Adding 'school_name' column to 'admin' table...")
            # SQLite specific ALTER TABLE
            cursor.execute("ALTER TABLE admin ADD COLUMN school_name VARCHAR(200) NOT NULL DEFAULT 'Bayero University Kano'")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column 'school_name' already exists.")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_schema()
