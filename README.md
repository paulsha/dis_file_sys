# Distributed File System
- **Paul Shanahan** - MAI Computer Engineering

Distributed file system for TCD Module CS7NS1 - Scalable Computing.

This file system is implemented using Python with a small number of additional packages.
The file system was created in a Windows environment.


The distributed file system implements 6 features (out of a possible 7) outlined at:
-[Specification](https://www.scss.tcd.ie/Stephen.Barrett/teaching/CS4400/individual_project.html) - TCD Credentials Required

These features are:
1. Distributed Transparent File Access (the Client)
2. Directory Service
3. Security Service
4. Lock Service
5. Caching
6. Replication


### System Requirements

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

### Directory Service
The Directory Service (dir_serv) is the handler of any information passing between the client and the file servers.
Any updates to the servers are done via HTTP Restful commands (i.e. POST, GET).
The directory service acts as a global handler for any servers, meaning that in the case of a file SEARCH the dir_serv only needs a filename and not its absolute or relative path.

### Security Service
The Security Service (sec_serv) acts as the sentry for the file system, handling user authentication, database encripytion and the encryption token used in subsequent client interactions. 
The user encrypted data is returned in JSON format and contains a user session key which can only be decrypted with the server key.
This is a standard form of encryption using private keys.
Database encrpytion can be seen by opening the database.db file created on first use of the file system. The data stored is not in raw format.

### Lock Service
The Lock Service (lock_serv) takes ownership of a file and prevents other users from accessing it.
This is done using a semaphore. The user who locks the file first can make as many ammendments as they wish for as long as they want (provided timeout does not occur on their session).
Other users who atttempt to access the file during this period will be informed that it is currently locked. Once the user UNLOCKS the file, it is then available to all users.
The LIST command lists all locked files. CHECK displays which user currently has the lock.

### Replication Server
Any new files added to a file server will be replicated across all servers.
If a user edits the backup, that will not impact the state of the primary file. 
Simiarly, edits of the backup can occur when the primary file is locked. So in other words,
the backup created when a file is added is more of a recovery checkpoint in case the primary file subsequently becomes corrupted or the server crashes.

### Caching
The system is configured in a RESTful format so that JSON objects are returned for editing.
This has an innate advantage in that caching is occuring as JSON objects are returned. When a file is opened, the details are stored locally in memory from the JSON object.
As such, any changes to the file occur locally on the client system before being pushed back to the server when the file is UNLOCKED. This is much quicker than working on the "remote" file directly for each ammendment.
