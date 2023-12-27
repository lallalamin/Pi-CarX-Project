import socket # for implementing our server and client to communicate over the network
import keyboard # setting keyboard to key, allowing us to use keyboard inputs 

def client():
    """
    Creates connection with the socket and binds it to the IP address and the given port number to listen on
    Initiates keyboard input
    """
    clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSock.connect(('10.103.16.84', 12000)) #IP address for our PiCar: 10.103.16.84 (Fern IP) We have to change IP address according to where we are
    print("Connected to server")

    while True: # will run continuously waiting for input
        key = keyboard.read_event(suppress=True).name 
        #Variable 'key' set to store keyboard events and relay 
        #them over the network via the server, then decides whether or not they were valid
        if key == 'esc':
            break #Exiting the while loop, closing the connection
        clientSock.send(key.encode())
    print("Connection closed")
    clientSock.close() #Closting the server/client connection

if __name__ == '__main__':
    client()