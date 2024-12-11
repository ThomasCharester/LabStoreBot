import sqlite3
import telebot

bot = telebot.TeleBot('6824237892:AAEf_2B1Ohlh7lgziz9e76xSgJiVoC-T9Q0')

superChatID = 69
onChatIDSet = False
onExecuteCommand = False

usersThreads = list((('SeregaPirat',69,69),('PeregaSirat',69,69)))

def writeUsersToFile():
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

def readUsersFromFile():
    global usersThreads

    connection = sqlite3.connect('usersThreads.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM Users')
    usersThreads = cursor.fetchall()

    connection.commit()
    connection.close()

def startDB():
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
    connection.close()


def removeUser(username):
    global usersThreads
    usersThreads.remove()
    
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

def debugGroupChat(spam):
    if(superChatID != 69): 
        bot.send_message(superChatID, spam)

startDB()

@bot.message_handler(commands = ['closeChat','cch'])
def main(message):
    if(message.chat.id != superChatID or superChatID == 69): 
        return
    bot.close_forum_topic(superChatID,message.message_thread_id)
    
@bot.message_handler(commands = ['deleteChat','dch'])
def main(message):
    if(message.chat.id != superChatID or superChatID == 69): 
        return
    bot.delete_forum_topic(superChatID,message.message_thread_id)

@bot.message_handler(commands = ['end'])
def main(message):
    if(message.chat.id != superChatID or superChatID == 69): 
        return
    
    debugGroupChat('Сохраняю прогресс')
    
    bot.stop_bot()

    quit()


@bot.message_handler(commands = ['start'])
def main(message):
    if(message.chat.id == superChatID or superChatID == 69): 
        return
    elif(message.from_user.username == getUsername(userchatid = message.chat.id)):
        bot.send_message(message.chat.id, 'Уже создана ветка')
        return
    
    id = bot.create_forum_topic(superChatID, message.from_user.username).message_thread_id
    
    addUserToDB(message.from_user.username,message.chat.id,id)
    debugGroupChat(getUsername(userchatid = message.chat.id))
    debugGroupChat(getUserThreadID(username=message.from_user.username))
    debugGroupChat(getUsername(threadid=id))


@bot.message_handler(commands = ['setGroup','sg'])
def main(message):
    if(message.chat.id != superChatID and superChatID != 69): 
        return
    
    global onExecuteCommand
    onExecuteCommand = True

    global onChatIDSet
    onChatIDSet = True
    bot.send_message(message.chat.id, 'Введите ID господин')

@bot.message_handler(commands = ['setGroupThis','sgt'])
def main(message):
    global superChatID

    if(message.chat.id != superChatID and superChatID != 69): 
        return
    
    superChatID =  message.chat.id
    bot.send_message(message.chat.id, 'Я глупенький хихи')

@bot.message_handler(commands = ['getChatID', 'cid'])
def main(message):
    if(message.chat.id != superChatID or superChatID == 69): 
        return
    
    bot.send_message(message.chat.id, message.chat.id, message_thread_id= message.message_thread_id)
    bot.send_message(message.chat.id, message.message_thread_id, message_thread_id= message.message_thread_id)
        
@bot.message_handler(commands = ['messageInfo','minfo'])
def main(message):
    if(message.chat.id != superChatID or superChatID == 69): 
        return
    
    bot.send_message(message.chat.id, message, message_thread_id= message.message_thread_id)

@bot.message_handler(commands = ['getUserID', 'uid','getUID'])
def main(message):
    if(message.chat.id != superChatID or superChatID == 69): 
        return
    
    bot.send_message(message.chat.id, message.from_user.id, message_thread_id= message.message_thread_id)

@bot.message_handler()
def main(message):
    if(superChatID == 69): 
        return
    global onExecuteCommand
    if(onExecuteCommand == True):
        executeCommand(message)
    elif(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_message(getUserThreadID(threadid = message.message_thread_id), message.text)
    elif(message.chat.id != superChatID and getThreadID(username= message.from_user.username) != None):
        bot.send_message(superChatID,message.text,message_thread_id=getThreadID(username= message.from_user.username))

def executeCommand(message):
    global onExecuteCommand
    
    global onChatIDSet
    global superChatID
    if(onChatIDSet == True and message.text == 'this'):
        onChatIDSet = False
        superChatID =  message.chat.id
    elif(onChatIDSet == True ):
        onChatIDSet = False     
        superChatID =  int(message.text)
    
    onExecuteCommand = False
    

bot.polling(none_stop=True)

