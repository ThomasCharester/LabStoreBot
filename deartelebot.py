import sqlite3
import telebot
from  telebot import types

bot = telebot.TeleBot('6824237892:AAEf_2B1Ohlh7lgziz9e76xSgJiVoC-T9Q0')

defaultInteger = -69
defaultUser = ('SeregaPrirat',defaultInteger,defaultInteger)

superChatID = defaultInteger
onChatIDSet = False
onExecuteCommand = False

usersThreads = list((('SeregaPirat',defaultInteger,defaultInteger),('PeregaSirat',defaultInteger,defaultInteger)))

def pythonMoment():
    global usersThreads
    usersThreads.remove(usersThreads[0])
    usersThreads.remove(usersThreads[0])

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
    
    cursor.execute('SELECT * FROM UsersThreads')
    connection.commit()
    
    usersThreads = cursor.fetchall()

    connection.commit()
    connection.close()

def getUser(username = defaultUser[0],userchatid = defaultUser[1],threadid = defaultUser[2]):
    userToSeek = (username,userchatid,threadid)

    if userToSeek[0] != defaultUser[0] and userToSeek[1] != defaultUser[1] and userToSeek[2] != defaultUser[2]:
        if userToSeek in usersThreads :
            return userToSeek
        else:
            return -1
    else:
        for user in usersThreads:
            if user[0] == username or user[1] == userchatid or user[2] == threadid:
                return user
        return -1
    
def removeUser(username = defaultUser[0],userchatid = defaultUser[1],threadid = defaultUser[2]):
    global usersThreads

    userToDelete = getUser(username ,userchatid,threadid)

    if userToDelete != -1:
        usersThreads.remove(userToDelete)

    
def addUser(username,userchatid,threadid):
    if getUser(username ,userchatid,threadid) == -1:
        usersThreads.append((username,userchatid,threadid))

def debugGroupChat(spam):
    if(superChatID != defaultInteger): 
        bot.send_message(superChatID, spam)

pythonMoment()
readUsersFromFile()

@bot.message_handler(commands = ['closeChat','cch'])
def main(message):
    if(message.chat.id != superChatID or superChatID == defaultInteger): 
        return
    bot.close_forum_topic(superChatID,message.message_thread_id)
    removeUser(threadid=message.message_thread_id)
    
@bot.message_handler(commands = ['deleteChat','dch'])
def main(message):
    if(message.chat.id != superChatID or superChatID == defaultInteger): 
        return
    bot.delete_forum_topic(superChatID,message.message_thread_id)

@bot.message_handler(commands = ['end'])
def main(message):
    if(message.chat.id != superChatID or superChatID == defaultInteger): 
        return
    
    writeUsersToFile()
    debugGroupChat('Сахраняю пагрес :3')
    
    bot.stop_bot()

    quit()


@bot.message_handler(commands = ['start'])
def main(message):
    if(message.chat.id == superChatID or superChatID == defaultInteger): 
        return
    elif(getUser(username=message.from_user.username) != -1):
        bot.send_message(message.chat.id, 'Уже создана ветка')
        return
    
    id = bot.create_forum_topic(superChatID, message.from_user.username).message_thread_id
    
    addUser(message.from_user.username,message.chat.id,id)
    debugGroupChat(getUser(userchatid = message.chat.id)[0])
    debugGroupChat(getUser(username=message.from_user.username)[1])
    debugGroupChat(getUser(threadid=id)[2])


@bot.message_handler(commands = ['setGroup','sg'])
def main(message):
    if(message.chat.id != superChatID and superChatID != defaultInteger): 
        return
    
    global onExecuteCommand
    onExecuteCommand = True

    global onChatIDSet
    onChatIDSet = True
    bot.send_message(message.chat.id, 'Введите ID господин')

@bot.message_handler(commands = ['setGroupThis','sgt'])
def main(message):
    global superChatID

    if(message.chat.id != superChatID and superChatID != defaultInteger): 
        return
    
    superChatID =  message.chat.id
    bot.send_message(message.chat.id, 'Я глупенький хихи')

@bot.message_handler(commands = ['getChatID', 'cid'])
def main(message):
    if(message.chat.id != superChatID or superChatID == defaultInteger): 
        return
    
    bot.send_message(message.chat.id, message.chat.id, message_thread_id= message.message_thread_id)
    bot.send_message(message.chat.id, message.message_thread_id, message_thread_id= message.message_thread_id)
        
@bot.message_handler(commands = ['messageInfo','minfo'])
def main(message):
    if(message.chat.id != superChatID or superChatID == defaultInteger): 
        return
    
    bot.send_message(message.chat.id, message, message_thread_id= message.message_thread_id)

@bot.message_handler(commands = ['getUserID', 'uid','getUID'])
def main(message):
    if(message.chat.id != superChatID or superChatID == defaultInteger): 
        return
    
    bot.send_message(message.chat.id, message.from_user.id, message_thread_id= message.message_thread_id)

@bot.message_handler(content_types= ['text'])
def main(message):
    if(superChatID == defaultInteger or getUser(username= message.from_user.username) == -1): 
        return
    global onExecuteCommand
    if(onExecuteCommand == True):
        executeCommand(message)
    elif(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_message(getUser(threadid = message.message_thread_id)[1], message.text)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_message(superChatID,message.text,message_thread_id=getUser(username= message.from_user.username)[2])

@bot.message_handler(content_types= ['photo'])
def main(message):
    if(superChatID == defaultInteger): 
        return
    global onExecuteCommand
    if(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_photo(getUser(threadid = message.message_thread_id)[1], message.photo[-1].file_id, caption = message.caption)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_photo(superChatID,message.photo[-1].file_id, caption = message.caption,message_thread_id=getUser(username= message.from_user.username)[2])

@bot.message_handler(content_types= ['video'])
def main(message):
    if(superChatID == defaultInteger): 
        return
    global onExecuteCommand
    if(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_video(getUser(threadid = message.message_thread_id)[1], message.video.file_id, caption = message.caption)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_video(superChatID,message.video.file_id, caption = message.caption,message_thread_id=getUser(username= message.from_user.username)[2])

@bot.message_handler(content_types= ['voice'])
def main(message):
    if(superChatID == defaultInteger): 
        return
    global onExecuteCommand
    if(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_voice(getUser(threadid = message.message_thread_id)[1], message.voice.file_id, caption = message.caption)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_voice(superChatID,message.voice.file_id, caption = message.caption,message_thread_id=getUser(username= message.from_user.username)[2])

@bot.message_handler(content_types= ['document'])
def main(message):
    if(superChatID == defaultInteger): 
        return
    global onExecuteCommand
    if(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_document(getUser(threadid = message.message_thread_id)[1], message.document.file_id, caption = message.caption)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_document(superChatID,message.document.file_id, caption = message.caption,message_thread_id=getUser(username= message.from_user.username)[2])

@bot.message_handler(content_types= ['audio'])
def main(message):
    if(superChatID == defaultInteger): 
        return
    global onExecuteCommand
    if(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_audio(getUser(threadid = message.message_thread_id)[1], message.audio.file_id, caption = message.caption)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_audio(superChatID,message.audio.file_id, caption = message.caption,message_thread_id=getUser(username= message.from_user.username)[2])

@bot.message_handler(content_types= ['sticker'])
def main(message):
    if(superChatID == defaultInteger): 
        return
    global onExecuteCommand
    if(message.chat.id == superChatID and message.message_thread_id != 0):
        bot.send_sticker(getUser(threadid = message.message_thread_id)[1], message.sticker)
    elif(message.chat.id != superChatID and getUser(username= message.from_user.username)[2] != None):
        bot.send_sticker(superChatID,message.sticker,message_thread_id=getUser(username= message.from_user.username)[2])

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

