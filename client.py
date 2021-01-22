import socket
import threading
import time
# create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 5050

# connection to hostname on the port.                            
# Receive no more than 1024 bytes

def respond():
    connection = True
    while connection:
        answer = client.recv(1024).decode("ascii")
        if answer == '!disconnect':
            connection = False
        print(f'{answer}')

LAUNCHED = threading.Thread(name='background', target=respond)

def chat_system():
    here = True
    while here:
        chat = input()
        client.send(chat.encode('ascii'))
        if chat == '!disconnect':
            print('You have been disconnected')
            time.sleep(2)
            here = False

user_name = input("Choose your Username: ")
client.connect((host, port)) 
client.send(user_name.encode('ascii'))
LAUNCHED.start()
chat_system()
