from flask_api import FlaskAPI
from flask import request, json
import SecurityService as sec_serv
import base64
app = FlaskAPI(__name__)
locked_files_list = []
server_key = 'lock_key_1'

#lock file
@app.route('/lock', methods=['POST'])
def lock_file():
    new_file = request.json
    for file in locked_files_list:
        if file['filename'] == new_file['filename']:
            return json.dumps(True)
    locked_files_list.append(new_file)
    return json.dumps(False)

#unlock a file
@app.route('/unlock', methods=['POST'])
def unlock_file():
    encrpytion_Request = request.json
    ticket = encrpytion_Request['ticket']
    sec_servKey = sec_serv.decrypt(base64.urlsafe_b64decode(ticket).decode(), server_key)
    new_file = json.loads(sec_serv.decrypt(encRequest['file'], sec_servKey))
    for file in locked_files_list:
        if file['filename'] == new_file['filename']:
            locked_files_list.remove(file)
            return 'Lock Lifted'

#retrieve owner
@app.route('/check/<filename>', methods=['GET'])
def check_file_owner(filename):
    for file in locked_files_list:
        if file['filename'] == filename:
            return str(filename + " locked by: " + file['userId'])
    return 'File does not exist/unlocked'

if __name__=='__main__':
    app.run(port=5003)