import sqlite3

conn = sqlite3.connect("test.db")

conn.execute("""CREATE TABLE test2(
            username text,
            passwd text,
            age integer
            )""")
