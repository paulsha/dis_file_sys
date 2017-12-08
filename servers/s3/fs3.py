from flask_api import FlaskAPI, status
from flask import request
import json
import os
import base64
app = FlaskAPI(__name__)

SERVER_NAME = 'Server: 3'
file_path = 'files/'

@app.route('/write', methods=['POST'])
def wf():
    updated_file = request.json
    filename = updated_file['filename']
    try:
        new_content = updated_file['file_content']
        file = open(os.path.join(file_path, filename), "wb+")
        file.write(new_content.encode())
    except:
               return {'File Not Found.'}, status.HTTP_404_NOT_FOUND
    return {'filename': filename, 'message': 'File successfully written.'}
	
@app.route('/open/<filename>', methods=['GET'])
def rf(filename):
    try:
        file = open(os.path.join(file_path, filename))
        content = file.read()
    except:
        return {'File Not Found.'}, status.HTTP_404_NOT_FOUND
    return {'filename': filename, 'file_content': content, 'server_port': '5008'}
	
@app.route('/find/<filename>', methods=['GET'])
def of(filename):
    try:
        open(os.path.join(file_path, filename))
    except:
        return {'File Not Found.'}, status.HTTP_404_NOT_FOUND
    return {'Server: ': SERVER_NAME,'file_path': '/'+file_path}
if __name__=='__main__':
    app.run(port=5009)