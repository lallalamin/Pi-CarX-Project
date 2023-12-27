import socket # for implementing our server and client to communicate over the network
from picarx import Picarx #allows us to access and use the files on the raspberry-pi, allowing a connection and use the movement functions
import time # for implementing the movement of the picar
from robot_hat import TTS #allows us to make the robot talk by text to speech
tts_robot = TTS()
tts_robot.lang("en-US")

def server():
    """
    Creates connection with the socket and binds it to the IP address and the given port number to listen on
    Initiates movement based on keyboard input
    """
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSock.bind(('', 12000)) #Listening for IP address of Picar and comparing correct port number from client
    serverSock.listen(1)
    print('Server listening on port 12000')

    while True:
        clientSock, address = serverSock.accept()
        print('Connection from', address) # shows that a connection has been made with the client
        while True:
            # will run until a non-key input is entered or the 'q' is pressed; exiting the loop and closing the server
            key = clientSock.recv(1024).decode() #Decoding key presses sent over the network from the client
            if not key or key == 'q':
                break #Exiting the loop
            handle_key(key)
        print('Connection closed')
        clientSock.close() #Closting the server/client connection

class Movement:
    """
    Holds all of the functions that move the picar with key press of the w, a, s, d, c keys
    Prints on function that is being run (direction it is moving) and saying what the action is doing
    Continually be accessed while server is running
    """
    def move_forward(self):
        print('Moving forward')
        tts_robot.say('Running Forward') #Saying it is running forward
        picar = Picarx()
        picar.forward(25) #Call to move the motors
        time.sleep(0.5)

    def move_backward(self):
        print('Moving backward')
        tts_robot.say('Backing Backing') #Saying it is backing up
        picar = Picarx()
        picar.forward(-25) #Call to move the motors (In negative direction to move backwards)
        time.sleep(0.5)

    def turn_right(self):
        print('Turning right')
        tts_robot.say('Turning right') #Saying it is turning right
        picar = Picarx()
        for i in range(0, 35): #for loop checking between that ranges that the wheel will turn when d is pressed
            picar.set_dir_servo_angle(i) #Call for turning the wheels, moving the servos
            time.sleep(0.05)

    def turn_left(self):
        print('Turning left')
        tts_robot.say('Turning left') #Saying it is turning left
        picar = Picarx()
        for i in range(-35, 0): #for loop checking between that ranges that the wheel will turn when a is pressed
            picar.set_dir_servo_angle(i) #Call for turning the wheels, moving the servos
            time.sleep(0.05)

    def stop_run(self):
        print('stop')
        picar = Picarx()
        picar.forward(0) #Call to stop the motors
        tts_robot.say('I am stopping') #Saying that it is stopping 
        time.sleep(0.5)

Input = Movement() # use key presses sent and decoded over the network
def handle_key(key):
    # determines which of the functions in the Movement class is being called
    if key == 'w':
        Input.move_forward()
    elif key == 's':
        Input.move_backward()
    elif key == 'a':
        Input.turn_left()
    elif key == 'd':
        Input.turn_right()
    elif key == 'c':
        Input.stop_run()
    else:
        print(f'Unknown key: {key}') #If not w, a, s, d, c key, loop will continue but no action will be done until valid key is pressed

if __name__ == '__main__':
    server()