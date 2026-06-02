import sqlite3
db = sqlite3.connect('test.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age INTEGER,
            name TEXT,
            gender TEXT);
            ''')
db.commit()

def insert_db(data):
    cursor.execute("INSERT INTO users(age, name, gender) VALUES('{0}', '{1}', '{2}')".format(data[0], data[1], data[2]))
    db.commit()

count = int(input('How many users do you want to add? '))
for i in range(count):
    x = int(input("How are you old?: "))
    y = (input("What is your name?: "))
    z = (input("What is your gender?: "))
    data = [x, y, z]
    insert_db(data)

cursor.execute("SELECT * FROM users")
result = cursor.fetchall()
#result = cursor.fetchmany(2)
#result = cursor.fetchone()
print(result)

cursor.execute("INSERT INTO users (name)"
                "VALUES ('Anna')")