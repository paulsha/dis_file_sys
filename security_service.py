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
def generateKey(N):
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