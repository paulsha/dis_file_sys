#
#
# This is the Chat Server Client. This hosts the UI for the client and enables interaction with the components of the
# distributed file system via the command line.
#
#


import re
import sec_serv as ss
import base64, json, requests, sys


#
#List of Available Commands
#
commands = "\nSEARCH <filename> \n LOCK <filename> \n UNLOCK <filename> \n READ <filename> \n WRITE <filename> <new content> \
           \n CHECK <filename> \n ADD <filename> <file server> \n LIST \n HELP \n QUIT"

sec_serv_url = 'http://127.0.0.1:5001/'
dir_serv_url = 'http://127.0.0.1:5002/'
locking_serv_url = 'http://127.0.0.1:5003/'

#
# Main Function
#
def main():

    # user login, each new client will be asked to log on, their details will then be stored in the SQL database
    user_ID = input("Please Enter Username: ")
    userPassword = input("Please Enter Password: ")

    encId = base64.urlsafe_b64encode(ss.encrypt(user_ID, userPassword).encode()).decode()

    print('Accessing Security Service')
    authDirJson = {'user_id': user_ID, 'password': userPassword, 'encrypted_id': encId, 'server_id': 'directory_key_1'}
    authLockJson = {'user_id': user_ID, 'password': userPassword, 'encrypted_id': encId, 'server_id': 'lock_key_1'}


    dir_req = requests.post(sec_serv_url+'auth', json=authDirJson)
    enc_dir_token = dir_req.json()['token']
    dec_dir_token = json.loads(ss.decrypt(base64.urlsafe_b64decode(enc_dir_token).decode(), userPassword))
    #print(dec_dir_token)

    lock_req = requests.post(sec_serv_url+'auth', json=authLockJson)
    enc_lock_token = lock_req.json()['token']
    dec_lock_token = json.loads(ss.decrypt(base64.urlsafe_b64decode(enc_lock_token).decode(), userPassword))
    #print(dec_lock_token)

    opened_files = []
    connected = True
    print("Welcome to a Distributed File Server. For a list of action commands, type HELP.")
    while connected:
        cmd = input("Please Enter Command >: ")
        m = re.search(r' $', cmd)

        if m is not None:
            print ("Try again but this time without the extra space!")

        elif cmd == "HELP":
            get_help()

        elif cmd == "QUIT":
            print("Goodbye!")
            quit(opened_files, dec_lock_token)

        elif "SEARCH" in cmd:
            filename = cmd.split()[1]
            read_file = requests.get(dir_serv_url+"get_directory/"+filename)
            print(read_file.text)

        elif "LOCK" in cmd:
            filename = cmd.split()[1]
            opened_files, msg = open(opened_files, filename, user_ID, dec_dir_token)
            print(msg)

        elif "UNLOCK" in cmd:
            filename = cmd.split()[1]
            opened_files, msg = close(opened_files, filename, dec_lock_token)
            print(msg)

        elif "READ" in cmd:
            filename = cmd.split()[1]
            file = read(opened_files, filename)
            print(file)

        elif "WRITE" in cmd:
            filename = cmd.split()[1]
            if len(cmd.split()) > 2:
                content = cmd.split(' ', 2)[2]
                msg = write(opened_files, filename, content, dec_dir_token)
                print(msg)
            else:
                print('WRITE requires two arguments, <filename> and  <updated content>')

        elif "ADD" in cmd:
            filename = cmd.split()[1]
            if len(cmd.split()) > 2 :
                filepath = cmd.split(' ', 2)[2]
                msg = add(filename, filepath, dec_dir_token)
                print(msg)
            else:
                print('ADD requires two arguments, <filename> and  <file server>')

        elif "LIST" in cmd:
            if len(opened_files) > 0:
                print(opened_files)
            else:
                print("No files opened.")

        elif "CHECK" in cmd:
            filename = cmd.split()[1]
            check = requests.get(locking_serv_url+"check/"+filename)
            print(check.text)

        else:
            print("Please provide correct commands, for more information on the commands, type HELP"
                  "\nMake sure to include file extensions in name (i.e. .txt etc)")

#	
#Get Help
#
def get_help():
    return print("You asked for help, heres a list of all commands: ", commands)
#	
#Write File	
#
def open(opened_files, filename, user_ID, token):
    for file in opened_files:
        if file['filename'] == filename:
            return opened_files, 'File already opened.'
    sessKey = token['session_key']
    file = {'filename': filename, 'user_ID': user_ID}
    open_json = {'file': ss.encrypt(json.dumps(file), sessKey), 'ticket': token['ticket']}
    open_file = requests.post(dir_serv_url + "open", json=open_json)
    if open_file.status_code != 200:
        return opened_files, open_file.text.strip('{}')
    opened_files.append(open_file.json())
    return opened_files, 'File successfully locked.'
#	
#Close File	
#
def close(opened_files, filename, token):
    for file in opened_files:
        if file['filename'] == filename:
            sessKey = token['session_key']
            close_json = {'file': ss.encrypt(json.dumps(file), sessKey), 'ticket': token['ticket']}
            close = requests.post(locking_serv_url+"unlock", json=close_json)
            opened_files.remove(file)
            return opened_files, "File successfully unlocked."
    return opened_files, "Error: No file of such name is opened."
#	
#Add File	
#	
def add(filename, filepath, token):
    sessKey = token['session_key']
    file = {'filename': filename, 'filepath': filepath}
    add_json = {'file': ss.encrypt(json.dumps(file), sessKey), 'ticket': token['ticket']}
    post = requests.post(dir_serv_url+"add", json=add_json)
    return post.text
#	
#Quit App
#
def quit(opened_files, token):
    for file in opened_files:
        sessKey = token['session_key']
        close_json = {'file': ss.encrypt(json.dumps(file), sessKey), 'ticket': token['ticket']}
        close = requests.post(locking_serv_url+"unlock", json=close_json)
        opened_files.remove(file)
    sys.exit()
#	
#Read File	
#
def read(opened_files, filename):
    for file in opened_files:
        if file['filename'] == filename:
            return file['file_content']
    return "Error: No file of such name is opened."
#	
#Write File	
#
def write(opened_files, filename, content, token):
    for file in opened_files:
        if file['filename'] == filename:
            sessKey = token['session_key']
            file['file_content'] = content
            open_json = {'file': ss.encrypt(json.dumps(file), sessKey), 'ticket': token['ticket']}
            updated_file = requests.post(dir_serv_url+"write", json=open_json)
            return updated_file.text
    return "Error: No file of such name is opened."

if __name__ == "__main__":
    main()