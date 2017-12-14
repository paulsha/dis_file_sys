# Distributed File System
- **Paul Shanahan** - MAI Computer Engineering

Distributed file system for TCD Module CS7NS1 - Scalable Computing.

This file system is implemented using Python with a small number of additional packages.
The file system was created in a Windows environment.


The distributed file system implements all seven features (4 minimum required for the assignment) outlined at:
-[Specification](https://www.scss.tcd.ie/Stephen.Barrett/teaching/CS4400/index.html) - TCD Credentials Required

These features are:
1. Distributed Transparent File Access (the Client)
2. Security Service
3. Directory Service
4. Lock Service
5. Caching
6. Replication
7. File Server

### System Requirements
```
* Python must be installed and available in the termianl using 'python'. The file system was built using Python 3.6.3 in a Windows environment.
* Once Python is installed, the following packages are also required: flask_api, requests.
```
pip install flask_api
pip install requests
```

### Running the File Server

1. Clone this repo.
2. Install additional packages required by python detailed above.
3. Run each .py file in the root directory ensuring that the client is initialised last.
```
python start_server1.py etc.
```
4. Enter any username and password to the client window. This is stored securely an SQL DB.
5. Follow the instructions provided for the command line interface.


### Distributed Transparent File Access (the Client)
Client.py acts as the UI for the file server. When the client is initialised,
the user is prompted to enter a username and password. This username and password is sent to the Security Service (sec_serv) for processing.
The Security Service acts as the sentry of the file system. Once the username and password have been processed,
the security service returns a token containing the session key. This key used for any further contact between the client and Directory Service (dir_serv).
This method ensures that the data passed from the client to the server is encrypted and not open for easy interception.

Within the HELP section of the client.py command line, you will find a list of all commands available to you.
* SEARCH <filename.x>; Returns file location.
* LOCK <filename.x>; Locks and caches file locally for user modification.
* UNLOCK <filename.x>; Reverse of OPEN.
* READ <filename.x>; Outputs content of the file to terminal.
* WRITE <filename.x> <Replacement text content>; Replaces content of the file with new user defined content.
* ADD <filename.x> <server>; Add a new file to a specific server, copies made in other servers.

* CHECK <filename.x>; Check the lock status of the file.
* LIST; Returns list of all locked files.
* HELP; Returns list of commands
* QUIT; Exits the system.


