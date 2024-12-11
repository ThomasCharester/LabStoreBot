import sqlite3

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Создаем таблицу Users
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
username TEXT NOT NULL PRIMARY KEY,
email TEXT NOT NULL,
age INTEGER
)
''')

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Добавляем нового пользователя
cursor.execute('INSERT OR REPLACE INTO Users (username, email, age) VALUES (?, ?, ?)', ('newuse2r', 'newuser@example.com', 28))

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()

# Устанавливаем соединение с базой данных
connection = sqlite3.connect('my_database.db')
cursor = connection.cursor()

# Выбираем всех пользователей
cursor.execute('SELECT * FROM Users')
users = cursor.fetchall()

# Выводим результаты
for user in users:
  print(user)

connection.commit()
# Закрываем соединение
connection.close()

usersThreads = list((('SeregaPirat',69,69),('PeregaSirat',69,69)))
connection = sqlite3.connect('usersThreads.db')
cursor = connection.cursor()
    
cursor.execute('SELECT * FROM Users')
usersThreads = cursor.fetchall()

connection.commit()
connection.close()

connection = sqlite3.connect('usersThreads.db')
cursor = connection.cursor()
    
cursor.execute('DROP TABLE UsersThreads')
connection.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS UsersThreads (
username TEXT NOT NULL PRIMARY KEY,
userchatid INTEGER NOT NULL,
threadid INTEGER
)
''')
connection.commit()
    
for user in usersThreads:
    cursor.execute('INSERT OR REPLACE INTO UsersThreads (username, userchatid, threadid) VALUES (?, ?, ?)', (user[0], user[1], user[2]))

connection.commit()
connection.close()

def removeUserFromDB(username):
    connection = sqlite3.connect('usersThreads.db')
    cursor = connection.cursor()

    cursor.execute('DELETE FROM UsersThreads WHERE username = ?', (username))

    connection.close()
    
def addUserToDB(username,userchatid,threadid):
    connection = sqlite3.connect('usersThreads.db')
    cursor = connection.cursor()

    cursor.execute('INSERT INTO UsersThreads (username, userchatid, threadid) VALUES (?, ?, ?)', (username, userchatid, threadid))

    connection.commit()
    connection.close()

def getUserThreadID(username = 'None', threadid = -69):
    connection = sqlite3.connect('usersThreads.db')
    cursor = connection.cursor()
    cursor.execute('SELECT userchatid FROM UsersThreads WHERE username = ? OR threadid = ?',(username, threadid))

    data = cursor.fetchone()
    connection.close()

    return data
    
def getUsername(userchatid = -69, threadid = -69):
    connection = sqlite3.connect('usersThreads.db')
    cursor = connection.cursor()
    cursor.execute('SELECT username FROM UsersThreads WHERE userchatid = ? OR threadid = ?',( userchatid, threadid))
    
    data = cursor.fetchone()
    connection.close()
    
    return data
    
def getThreadID(username = 'None', userchatid = -69):
    connection = sqlite3.connect('usersThreads.db')
    cursor = connection.cursor()
    cursor.execute('SELECT threadid FROM UsersThreads WHERE username = ? OR userchatid = ?',(username, userchatid))
    
    data = cursor.fetchone()
    connection.close()

    return data