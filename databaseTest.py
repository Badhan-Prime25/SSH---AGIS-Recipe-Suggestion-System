# this is to check the database is working
import sqlite3


conn = sqlite3.connect('foodDatabase.db')
cursor = conn.cursor()
print("Recipes Table:")
cursor.execute("SELECT * FROM Recipes;")
print(cursor.fetchall())


conn.close()