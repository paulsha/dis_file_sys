from flask_api import FlaskAPI, status
from flask import request
import requests, copy, json, base64
import sec_serv as ss

app = FlaskAPI(__name__)

file_server_url = 'http://127.0.0.1:'
server_key = 'directory_key_1'


@app.route('/get_directory/<filename>', methods=['GET'])
def get_directory(filename):
    for n in [5007, 5008]:
        server_url = file_server_url + str(n) + "/find/" + filename
        in_directory = requests.get(server_url)
        status_code = in_directory.status_code
        if status_code == 200:
            return in_directory.json()
    return {'Error:': 'File does not exist amongst servers.'}


@app.route('/open', methods=['POST'])
def of():
    encRequest = request.json
    ticket = encRequest['ticket']
    sessKey = ss.decrypt(base64.urlsafe_b64decode(ticket).decode(), server_key)
    file = json.loads(ss.decrypt(encRequest['file'], sessKey))
    for n in [5007, 5008]:
        server_url = file_server_url + str(n) + "/open?" + 'filename='+file['filename'] + '&userId='+file['userId']
        in_directory = requests.get(server_url)
        status_code = in_directory.status_code
        if status_code == 200:
            return in_directory.json()
        elif status_code == 409:
            return {'Error:': 'File is already locked.'}, status.HTTP_404_NOT_FOUND
    return {'Error:': 'File does not exist amongst servers.'}, status.HTTP_404_NOT_FOUND


@app.route('/write', methods=['POST'])
def wf():
    encRequest = request.json
    ticket = encRequest['ticket']
    sessKey = ss.decrypt(base64.urlsafe_b64decode(ticket).decode(), server_key)
    file = json.loads(ss.decrypt(encRequest['file'], sessKey))
    status_code = 0
    for n in [5007, 5008]:
        if str(n) == file['server_port']:
            print(file)
            server_url = file_server_url + str(n) + "/write"
            write = requests.post(server_url, json=file)
            status_code = write.status_code
        else:
            server_url = file_server_url + str(n) + "/write"
            backup = copy.copy(file)
            backup['filename'] = str(file['filename']).split('.')[0] + "_backup.txt"
            backup['server_port'] = str(n)
            print(backup)
            write_backup = requests.post(server_url, json=backup)
    if status_code == 200:
       return "File successfully upated."
    return 'Error: Unknown Error.'


@app.route('/add', methods=['POST'])
def af():
    encRequest = request.json
    ticket = encRequest['ticket']
    sessKey = ss.decrypt(base64.urlsafe_b64decode(ticket).decode(), server_key)
    file = json.loads(ss.decrypt(encRequest['file'], sessKey))
    status_code = 0
    for n in [5007, 5008]:
        server_name = requests.get(file_server_url + str(n) + "/name")
        if server_name.text == file['filepath']:
            add_file = requests.post(file_server_url + str(n) + "/add", json=file)
            status_code = add_file.status_code
        else:
            backup = copy.copy(file)
            backup['filename'] = str(file['filename']).split('.')[0] + "_backup.txt"
            backup['server_port'] = str(n)
            add_file = requests.post(file_server_url + str(n) + "/add", json=backup)
    if status_code == 200:
        return add_file.text
    return 'Error: No such server exists.'


if __name__=='__main__':
    app.run(port=5002)