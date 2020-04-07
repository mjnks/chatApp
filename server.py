#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clientInfo = dict()
# addresses = dict()

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def closeClient(clientSocket):
    """
    Closes given client's remote session if still running 
    Closes socket and removes it from dictionary 
    Notifies remaining clients
    """
    clientSocket.close()
    name = clientInfo[clientSocket]
    del clientInfo[clientSocket]
    # del addresses[clientSocket]
    broadcast(bytes("{} has left the chat.".format(name), "utf8"), "SERVER")
    print("{} has disconnected".format(name))

def socketSend(clientSocket, message):
    """
    The purpose of this wrapper for client.send is to handle errors if the client has 
    disconnected
    """
    try:
        # Attempt to send the client message
        clientSocket.send(message)
        return True
    except BrokenPipeError:
        # Could not send to this client, they have disconnected in an abnormal way
        # Ctrl-C, pressing the X in the window, power failure, etc.
        closeClient(clientSocket)
        return False

def acceptIncomingConnections():
    """Sets up handling for incoming clients."""
    while True:
        client, clientAddress = SERVER.accept()
        print("{}:{} has connected.".format(clientAddress[0], clientAddress[1]))
        socketSend(client, bytes("Greetings "+
                          "Now type your name and press enter!", "utf8"))
        # addresses[client] = clientAddress
        Thread(target=handleClient, args=(client,)).start()

def handleClient(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    socketSend(client, bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clientInfo[client] = name
    while True:
        try:
            msg = client.recv(BUFSIZ)
            if msg != bytes("{quit}", "utf8"):
                broadcast(msg, name)
            else:
                socketSend(client, bytes("{quit}", "utf8"))
                closeClient(client)
                break
        except OSError:
            # Do nothing, they sent a bad message
            pass

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    # Iterate over list of keys to avoid issues if client is deleted due to disconnection
    for sock in list(clientInfo):
        socketSend(sock, bytes(prefix + ": ", "utf8")+bytes(msg, "utf8"))
        

if __name__ == "__main__":
    SERVER.listen(5)  # Listens for 5 connections at max.
    print("Waiting for connection...")
    connectionHandler = Thread(target=acceptIncomingConnections)
    connectionHandler.start()  # Starts the infinite loop.
    connectionHandler.join()
    SERVER.close()