from flask_api import FlaskAPI
from flask import request, json
import sec_serv as ss
import base64

app = FlaskAPI(__name__)

locked_files = []
server_key = 'lock_key_1'

@app.route('/lock', methods=['POST'])
def lock():
    new_file = request.json
    for file in locked_files:
        if file['filename'] == new_file['filename']:
            return json.dumps(True)
    locked_files.append(new_file)
    return json.dumps(False)


@app.route('/unlock', methods=['POST'])
def unlock():
    encRequest = request.json
    ticket = encRequest['ticket']
    sessKey = ss.decrypt(base64.urlsafe_b64decode(ticket).decode(), server_key)
    new_file = json.loads(ss.decrypt(encRequest['file'], sessKey))
    for file in locked_files:
        if file['filename'] == new_file['filename']:
            locked_files.remove(file)
            return 'File unlocked.'


@app.route('/check/<filename>', methods=['GET'])
def check_owner(filename):
    for file in locked_files:
        if file['filename'] == filename:
            return str(filename + " is locked by user " + file['userId'])
    return 'This file is either not locked or does not exist.'

if __name__=='__main__':
    app.run(port=5003)