import sqlite3
import os

# Path to the database
params = {
    'db_path': os.path.join('instance', 'blockchain.db')
}

def check_admin_data():
    if not os.path.exists(params['db_path']):
        print(f"Database not found at {params['db_path']}")
        return

    conn = sqlite3.connect(params['db_path'])
    cursor = conn.cursor()

    try:
        print("Fetching all admins...")
        cursor.execute("SELECT id, username, email, school_name FROM admin")
        admins = cursor.fetchall()
        
        for admin in admins:
            print(f"{admin[0]}|{admin[1]}|{admin[2]}|{admin[3]}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    check_admin_data()
