# The chatApp Project
This is a simple project using TCP, multithreading, and python to create a server/client instant messaging application. We are using  [Write A Chat App in Python](https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac1701) as a reference for this project. It should take 1-2 hours to complete the project.

## Getting Started
******************
**Make sure your package repositories are up to date:**
```bash
sudo apt update && apt upgrade
```
**Make sure PIP3 and Virtual Environments are installed:**
```bash
sudo apt install python3-pip && python3-venv
```
**Create and Enter the Virtual Environment:** <br>
To create a virtual environment, pass the python3 interpreter the <code>venv</code> module (donted with the <code>-m</code> flag) and the desired name of the new environment:
```bash
python3 -m venv <environmentName>

EXAMPLE: python3 -m venv chatApp
```
This will create a new directory in the current folder with the same name as the virtual environment you just created. To enter the environment, invoke the <code>activate</code> binary in <code>./\<environmentName\>/bin/</code>
```bash
source <environmentName>/bin/activate
```
Upon success, the commandline prompt will update, indicating the user is in a virtual environment:
```bash
(<environmentName>) userprompt$
```
Once inside the virtual environment, install the required packages (*NOTE: Some packages may already be installed in the non-virtual environment, but they will not be available in the virtual environment until the installation commands are run.*):
```bash
pip3 install -r requirements.txt
```
Once the required packages are install, go to the link in the summary to get started. Use <code>server.py</code> for the server code and <code>client.py</code> for the client code.

## Running the app

**Install Python3 on local machine**</br>
**Run the client.py with the native python terminal**</br>
