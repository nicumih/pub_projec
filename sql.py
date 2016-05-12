import sqlite3 

with sqlite3.connect("sample.db") as connection:
    c = connection.cursor()
    c.execute("""CREATE TABLE questions(q TEXT, vots TEXT)""")
    c.execute('INSERT INTO questions VALUES("prima","test:test")')
    c.execute('INSERT INTO questions VALUES("doua","test:test")')          
    
    
