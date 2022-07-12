import sqlite3

def db_connection():
    #function to open a database connection

    conn = sqlite3.connect('backend_test.db')
    cursor = conn.cursor()

    return cursor

def function_filter(query,string):
    #function to filter the query
    #returns the new query

    rows = []
    if string != '*':
        for row in query:
            for r in row:
                if string in str(r):
                    rows.append(row)
                    break

        query = rows.copy()
    
    return query