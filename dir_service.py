from flask_api import FlaskAPI
import requests
import SecurityService as sec_serv

app = FlaskAPI(__name__)


file_server_url = 'http://127.0.0.1:'


@app.route('/read/<filename>', methods=['GET'])
def get_dir(filename):
    in_directory = requests.get(file_server_url+"5007/"+"read/"+filename)
    print(in_directory.text)
    status_code = in_directory.status_code
    if status_code == 200:
        return in_directory.json()
    else:
        return {'Error:': 'File does not exist amongst servers.'}


if __name__=='__main__':
    app.run(port=5002)