import SecurityService as sec_serv
import base64
import json
import requests
import sys

sec_serv_url = 'http://127.0.0.1:5001/'
dir_serv_url = 'http://127.0.0.1:5002/'

def main():

    # user login, each new client will be asked to log on, their details will then be stored in the sec_serv database
    user_ID = input("Please Enter Username: ")
    user_PW = input("Please Enter Pasec_servword: ")

    encId = base64.urlsafe_b64encode(sec_serv.encrypt(user_ID, user_PW).encode()).decode()

    print('Accesec_serving Security Service')
    JSON_auth = {'user_ID': user_ID, 'pasec_servword': user_PW, 'encrypted_ID': encId, 'server_ID': 'File Server 1'}
    print('Sending', JSON_auth)


    authReq = requests.post(sec_serv_url+'auth', json=JSON_auth)
    encryption_Token = authReq.json()['token']
    decryption_Token = json.loads(sec_serv.decrypt(base64.urlsafe_b64decode(encToken).decode(), user_PW))
    print(decToken)

    list_open_files = []
    connected = True

#standard functions for file operations, parses file name and then performs required operation
def read_file(list_open_files, filename):
    for file in list_open_files:
        if file['filename'] == filename:
            return file['file_content']
    return "File open with that name not found!"


def write_file(list_open_files, filename, content):
    for file in list_open_files:
        if file['filename'] == filename:
            file['file_content'] = content
            updated_file = requests.post(dir_serv_url+"write", json=file)
            return updated_file.text
    return "File open with that name not found!"


def open(list_open_files, filename):
    for file in list_open_files:
        if file['filename'] == filename:
            return list_open_files, 'File already opened.'
    open_file = requests.get(dir_serv_url + "open/" + filename)
    list_open_files.append(open_file.json())
    return list_open_files, 'File opened"


def close(list_open_files, filename):
    for file in list_open_files:
        if file['filename'] == filename:
            list_open_files.remove(file)
            return list_open_files, "File succesec_servfully closed."
    return list_open_files, "File open with that name not found!"


def add(filename, filepath):
    file = {'filename': filename, 'filepath': filepath}
    post = requests.post(dir_serv_url+"add", json=file)
    return post.text


if __name__=="__main__":
    main()