"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

clients   = {}
addresses = {}

HOST        =   ''
PORT        =   33000
BUFFERSIZE  =   1024 # ISSUE: This looks like it can break easily
ADDR        =   (HOST, PORT)
SERVER      =   socket(AF_INET, SOCK_STREAM)

SERVER.bind(ADDR)

def broadcast(msg, prefix=''):
    '''
    send a message to all clients currently connected to the server

    msg:    byte string with encoding. contains a message for the chatroom.
    prefix: standard string. Intended to contain a username.
    '''
    # convert the prefix to a byte string with encoding
    prefix = bytes(prefix, "utf8")

    # broadcast the message to connected clients
    for s in clients:
        s.send(prefix + msg)

def handle_client(client_socket):
    """
    Handles a single client connection

    client_socket: obj: client_socket
    """
    # get the username from the client and send the welcome message
    userName = client_socket.recv(BUFFERSIZE).decode("utf8")
    welcomeMessage = 'Welcome to JenkoChat {}, type \"{quit}\" to exit.'.format(userName)
    client_socket.send(bytes(welcomeMessage, "utf8"))
    
    # notify other users of the new client conection
    serverBulletin = "Notice: {} has connected to JenkoChat".format(userName)
    broadcast(bytes(serverBulletin, "utf8"))
    
    # add the new client to the client dictionary as {obj: client_socket:userName}
    clients[client_socket] = userName
    
    # handle incoming chatStrings from the client
    while True:
        # receive the chatString from the client
        chatString = client_socket.recv(BUFFERSIZE)
        # broadcast chatString to the JenkoChat chat room
        if chatString != bytes("{quit}", "utf8"):
            broadcast(chatString, userName+": ")

        # if the user sends the {quit} command,
        # terminate the connection and clean up
        else:
            client_socket.send(bytes("Goodbye!", "utf8"))
            client_socket.send(bytes("{quit}", "utf8"))
            client_socket.close
            del clients[client_socket]
            broadcast(bytes("{} abandoned JenkoChat. \
                                May they be scorned.".format(userName), "utf8"))
            break

def accept_incoming_connections():
        """
        set up handling for incoming client connections
        QUESTION:   How does this handle when there is no incoming connection? It can't
                    simply print the empty string all the time... how does it know
                    when to print and when not to print?
        """
        # continuously wait for incoming connections and handle them when they arrive
        while True:
            # accept the incoming connection and store 
            # (obj: client_socket, client_address (host_addr, port))
            client_socket, client_address = SERVER.accept()
            
            # log the new connection on the console shell running the server
            print("New Conection: %s:%s" % client_address)
            
            # send a message to the client using utf8 character encoding
            client_socket.send(bytes("Welcome to JenkoChat. \
                                    Please enter a username:", "utf8"))
            
            # add a dictionary element of {obj: client_socket:client_address}
            addresses[client_socket] = client_address
            
            # spawn a new thread to handle the client conection
            Thread(target=handle_client, args=(client_socket,)).start

if __name__ == "__main__":
    SERVER.listen(5)    # listens for up to five connections
    print("Waiting for connections...") # just a startup status message
    
    
    # spawn and start a new thread to handle incoming client connections
    CONNECTION_HANDLER = Thread(target=accept_incoming_connections)
    CONNECTION_HANDLER.start()
    
    # block this thread from continuing until the conection handler thread
    # terminates. If the join() times out and the thread is still alive,
    # call it again
    CONNECTION_HANDLER.join()
    while(CONNECTION_HANDLER.isAlive()):
        CONNECTION_HANDLER.join()
    
    # once the connection handler is dead, close the server down
    SERVER.close()