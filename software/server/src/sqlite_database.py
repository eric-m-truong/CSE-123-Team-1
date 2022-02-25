import sqlite3

DATA_DIR = '../data/'

connection = sqlite3.connect(DATA_DIR + 'users.sqlite')
cursor = connection.cursor()

# cursor.execute("""CREATE TABLE users (
#                 first text,
#                 last text,
#                 account_num integer
#                 )""")

cursor.execute("INSERT INTO users VALUES ('John', 'Smith', 0)")

# cursor.execute("SELECT * FROM users WHERE last='Smith'")
# print(cursor.fetchone())

connection.commit()

connection.close()  # Good practice to close