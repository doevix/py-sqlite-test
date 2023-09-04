#! /usr/bin/python3
import apsw
from matplotlib import pyplot as plt

# Define connection/file to database
db = apsw.Connection("mydb.db")
cursor = db.cursor()

# Fetch times
cursor.execute("SELECT time FROM sim_output")
time = cursor.fetchall()
# Fetch velocity results
cursor.execute("SELECT vel FROM sim_output")
vel = cursor.fetchall()

plt.plot(time, vel)
plt.show()
