#! /usr/bin/python3
import apsw

db = apsw.Connection("mydb.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS mytable(animal,sound)")

cursor.execute("SELECT * FROM mytable")
print(cursor.fetchall())

cursor.execute("SELECT * FROM mytable WHERE sound=?", ('woof',))
print(cursor.fetchall())
