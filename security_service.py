from flask import request
from flask_api import FlaskAPI
import sqlite3 as sql

import base64
import random
import json
import string

app = FlaskAPI(__name__)
db = sql.connect('database.db')
cursor = db.cursor()
#Retrive User PW
def getUserPassword(user_ID):
    cursor.execute('''SELECT password FROM users WHERE id=?''', (user_id,))
    data = cursor.fetchone()
    if data is None:
        return None
    return data[0]
	
#Verify User 
def VerifyUser(user_ID, encrpytion_ID):
    password = getPassword(user_id)
    if password is None:
        return False
    encryptedHere = encrypt(user_id, password)
    return base64.urlsafe_b64encode(encryptedHere.encode()) == enc_id

# random key
def generateRandKey(N):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
	
# encrypt/decrpyt data with cipher
def encrypt(data, key):
    enc = ''
    for i in range(len(data)):
        enc += chr(ord(data[i]) ^ ord(key[i % len(key)]) % 256)
    return enc
def decrypt(data, key):
    dec = ''
    enc = data
    for i in range(len(data)):
        dec += chr(ord(data[i]) ^ ord(key[i % len(key)]) % 256)
    return dec
	
+def get_db():
+    return db



@app.route('/auth', methods=['POST'])
def authenticatate():
    input = request.json
    user_ID = input['user_ID']
    encrpytion_ID = input['encrypted_ID'].encode()
    server_ID = input['server_ID']
    cursor.execute('''INSERT OR REPLACE INTO users(id, password, encrpytion_id) VALUES(?,?,?)''',
                   (input['user_ID'], input['password'], input['encrypted_ID']))
    cursor.execute('''INSERT OR REPLACE INTO servers(id, key) VALUES(?,?)''',
                   (input['server_ID'], input['server_ID']))
    db.commit()

    if VerifyUser(user_ID, enc_ID):
        key = getServerKey(server_ID)
        if key is None:
            return {'error': 'Server with specified key does not exist '}
        sessKey = generateKey(16)
        encSessKey = encrypt(sessKey, key)
        encSessKey = base64.b64encode(encSessKey.encode()).decode()
        token = {'ticket': encSessKey, 'session_key': sessKey, 'server_ID': server_id, 'timeout': 200 }
        encToken = base64.urlsafe_b64encode(encrypt(json.dumps(token), getPassword(user_id)).encode())
        return {'token': encToken.decode()}
    else:
        return {'error': 'User does not exist or encrpyted ID is wrong'}

if __name__=='__main__':
    createDB()
    app.run(port=5001)