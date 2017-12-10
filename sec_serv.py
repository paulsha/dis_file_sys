from flask import request
from flask_api import FlaskAPI

import sqlite3 as sql
import base64, random, json, string

app = FlaskAPI(__name__)

db = sql.connect('database.db')
cursor = db.cursor()


def get_database():
    return db


# encrypt the data according to the key using Vigenere cipher
def encrypt(data, key):
    enc = ''
    for i in range(len(data)):
        enc += chr(ord(data[i]) ^ ord(key[i % len(key)]) % 256)
    return enc


# decrypt the data according to the key using Vigenere cipher
def decrypt(data, key):
    dec = ''
    enc = data
    for i in range(len(data)):
        dec += chr(ord(data[i]) ^ ord(key[i % len(key)]) % 256)
    return dec


# get the password associated with this user for testing encryption
def getPassword(user_id):
    cursor.execute('''SELECT password FROM users WHERE id=?''', (user_id,))
    data = cursor.fetchone()
    if data is None:
        return None
    return data[0]


# checks the encrypted ID and checks if it belongs to that user
def isUser(user_id, enc_id):
    password = getPassword(user_id)
    if password is None:
        return False
    encryptedHere = encrypt(user_id, password)
    return base64.urlsafe_b64encode(encryptedHere.encode()) == enc_id


# generates a random session key of size N using capital letters and numbers
def generateKey(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))


# get the key associated with this server
def getServerKey(server_id):
    cursor.execute('''SELECT key FROM servers WHERE id=?''', (server_id,))
    data = cursor.fetchone()
    if data is None:
        return None
    return data[0]


# Creates the databases which store the users and servers
def createDB():
    cursor.execute('''CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, password TEXT, enc_id TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS servers(id TEXT PRIMARY KEY, key TEXT)''')
    db.commit()


@app.route('/auth', methods=['POST'])
def authenticate():
    input = request.json
    user_id = input['user_id']
    enc_id = input['encrypted_id'].encode()
    server_id = input['server_id']
    cursor.execute('''INSERT OR REPLACE INTO users(id, password, enc_id) VALUES(?,?,?)''',
                   (input['user_id'], input['password'], input['encrypted_id']))
    cursor.execute('''INSERT OR REPLACE INTO servers(id, key) VALUES(?,?)''',
                   (input['server_id'], input['server_id']))
    db.commit()

    if isUser(user_id, enc_id):
        key = getServerKey(server_id)
        if key is None:
            return {'error': 'No server with this key exists'}
        sessKey = generateKey(16)
        encSessKey = encrypt(sessKey, key)
        encSessKey = base64.urlsafe_b64encode(encSessKey.encode()).decode()
        token = {'ticket': encSessKey, 'session_key': sessKey, 'server_id': server_id, 'timeout': 200 }
        encToken = base64.urlsafe_b64encode(encrypt(json.dumps(token), getPassword(user_id)).encode())
        return {'token': encToken.decode()}
    else:
        return {'error': 'User does not exist or encrpyted ID is wrong'}



if __name__=='__main__':
    createDB()
    app.run(port=5001)
