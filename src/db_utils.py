import psycopg2
from psycopg2 import sql, Error
import os

def connect_db():
    try:
        conn = psycopg2.connect(database="task_manager_db",  
                                user=os.environ.get('DB_USER'), 
                                password=os.environ.get('DB_PASSWORD'),  
                                host="localhost", port="5432") 
        return conn, conn.cursor() 
    except (Exception, Error) as e:
        print('Failed to connect to db: ', e)
        return None, None

  
# initialises the db by creating the users and tasks tables
# if they don't already exist
def init_db() -> bool:
    conn, cur = connect_db()

    if not conn or not cur:
        return False
    
    try:
        # create the users table
        cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(100) NOT NULL,
                    last_name VARCHAR(100) NOT NULL,
                    created_at BIGINT
                );
            ''')
        # create the tasks table
        cur.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    priority INTEGER,
                    is_completed BOOLEAN DEFAULT FALSE,
                    completed_date BIGINT,
                    due_date BIGINT,
                    user_id INTEGER,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
            ''')

        conn.commit()
        print("Database initialised successfully.")
        return True
    
    except (Exception, Error) as e:
        print('Failed to initialise db: ', e)
        return False
    finally:
        cur.close() 
        conn.close()


# returns a table's contents, for debugging atm
def select_table(table : str) -> list:
    conn, cur = connect_db()
    # using SQL and formatting to avoid SQL injection
    query = sql.SQL('SELECT * from {}').format(sql.Identifier(table))
    cur.execute(query)
    results = cur.fetchall()
    cur.close() 
    conn.close()
    return results

# inserts a user into the users table
# TODO make the function usable for tasks too
def insert_user(user : dict) -> bool:
    conn, cur = connect_db()
    if not conn or not cur:
        return False
    
    if not isinstance(user, dict):
        return False

    try:
        query = 'INSERT INTO users (first_name, last_name, created_at) VALUES (%s, %s, %s);'
        cur.execute(query, (user['firstName'], user['lastName'], user['createdAt']))
        conn.commit()
        print("Table updated successfully.")
        return True
    except (Exception, Error) as e:
        print("Failed to update table: ", e)
        return False
    finally:
        cur.close() 
        conn.close()