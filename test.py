import sqlite3


connection = sqlite3.connect('usersThreads.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS UsersThreads (
username TEXT NOT NULL PRIMARY KEY,
userchatid INTEGER NOT NULL,
threadid INTEGER
)
''')
connection.commit()

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