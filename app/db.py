import sqlite3

# database - how to connect to it with python

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# define a schema
create_table = "CREATE TABLE users (id int, username text, password text)"

cursor.execute(create_table)

user = (1, 'Hannah', 'password')

insert_query = "INSERT INTO users VALUES (?, ?, ?)"


cursor.execute(insert_query, user)

users = [
    (2, 'Harrison', 'password'),
    (3, 'Charlie', 'password'),
    (4, 'Molly', 'password'),
    (5, 'Josh', 'password'),
    (6, 'Bexy', 'password')
]

cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)


connection.commit()

connection.close()