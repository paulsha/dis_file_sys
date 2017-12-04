from flask_api import FlaskAPI
import requests
import SecurityService as sec_serv
app = FlaskAPI(__name__)
fs_url = 'http://127.0.0.1:'

#series of functions to read,write,add and get directory for dir_service

@app.route('/write', methods=['POST'])
def wf(filename):
    for n in [5007, 5008]:
        server_url = fs_url+str(n)+"/"+"write/"+filename
        in_directory = requests.post(server_url)
        print(in_directory.text)
        status_code = in_directory.status_code
        if status_code == 200:
            return "File written"
    return {'Unknown Error Occured'}

@app.route('/open/<filename>', methods=['GET'])
def rf(filename):
    for n in [5007, 5008]:
        server_url = fs_url+str(n)+"/"+"open/"+filename
        in_directory = requests.get(server_url)
        print(in_directory.text)
        status_code = in_directory.status_code
        if status_code == 200:
            return in_directory.json()
    return {'File not found on any server.'}

@app.route('/add', methods=['POST'])
def af():
    file = request.json
    for n in [5007, 5008]:
        server_name = requests.get(file_server_url + str(n) + "/name")
        if server_name.text == file['filepath']:
            post = requests.post(file_server_url + str(n) + "/add", json=file)
            return post.text
    return 'No server'
	
@app.route('/get_dir/<filename>', methods=['GET'])
def get_dir(filename):
    in_directory = requests.get(fs_url+"5007/"+"read/"+filename)
    print(in_directory.text)
    status_code = in_directory.status_code
    if status_code == 200:
        return in_directory.json()
    else:
        return {'File not found on any server.'}
		
if __name__=='__main__':
    app.run(port=5002)