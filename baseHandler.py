import sqlite3 as sql
import json

connection = sql.connect('./base.sqlite', check_same_thread=False)
bd = connection.cursor()

bd.execute('''
CREATE TABLE IF NOT EXISTS users (
userid INTEGER,
state INTEGER,
answer INTEGER,
rating INTEGER
)
''')

def getRandCollection(count):
    req = bd.execute('SELECT * FROM cards ORDER BY RANDOM() LIMIT ?', (count, ))
    res = req.fetchall()
    return [list(i) for i in res]

def userIsExist(userid):
    req = bd.execute('SELECT * FROM users WHERE userid = ?', (userid,))
    res = req.fetchall()
    return len(res) > 0

def startUser(userid):
    bd.execute('INSERT INTO users (userid, state, answer, rating) VALUES (?,0,0,0)', (userid,))
    connection.commit()

def getUserAnswer(userid):
    req = bd.execute('SELECT answer FROM users WHERE userid = ?', (userid,))
    res = req.fetchall()
    return res[0][0]

def setAnswer(userid, answer):
    bd.execute('UPDATE users SET answer = ? WHERE userid = ?', (answer, userid))
    connection.commit()

def addRating(userid, scores):
    bd.execute('UPDATE users SET rating = rating + ? WHERE userid = ?', (scores, userid))
    connection.commit()

def getRating(userid):
    req = bd.execute('SELECT rating FROM users WHERE userid = ?', (userid,))
    res = req.fetchall()
    return res[0][0]