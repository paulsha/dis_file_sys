import SecurityService as sec_serv
import requests
import base64
import json


def main():
#read user input for username, password
	user_ID = input("Username: ")
    user_PW = input("Password: ")
	
#invoke base64 encoding so not raw text	
	encryption_ID = base64.urlsafe_b64encode(sec_serv.encrypt(user_ID, user_PW).encode()).decode()
	JSON_auth_init = {'user_ID': user_ID, 'password': user_PW, 'encrypted_id': encrpytion_ID, 'server_ID': 'Directory'}
	
	#POST JSON
	authReq = requests.post('http://127.0.0.1:5001/auth', json=JSON_auth_init)
	encryption_Token = authReq.json()['token']
    decryption_Token = json.loads(sec_serv.decrypt(base64.urlsafe_b64decode(encryption_Token).decode(), user_PW))
	#Print to Client
	print(decrpytion_Token)
	
#Def	
if __name__ == "__main__":
    main()