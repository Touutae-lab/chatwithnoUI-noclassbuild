import socket
import threading
import pickle
import datetime

now = datetime.datetime.now()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

f_length = 1024 #Byte weight
FORMAT = 'ascii' #Format file

active_client = {} #Active Client Remaining in Current Chat
list_a = [] #<issue Avoiding list>
host = socket.gethostname() #Get hostname
port = 5050 
member = [] #Issue Avoiding list
server.bind((host, port)) #bin server

#---------------------CHECK NAME--------------------------#
# def name_check():
#    data=pickle.dumps([i for i in active_client]) 
#    while True:
#       for i in active_client:
#          try:
#             active_client[i].send(data)
#          except ConnectionResetError:
#             pass
#
# namethread = threading.Thread(target=name_check)
# namethread.start()
#--------------------------------------------------------#


def client_management(client, addr):
   connection = True
   print(f'[SERVER] New connection from {addr}')
   usrname = client.recv(f_length).decode(FORMAT)
   #usrname = client.recv(f_length).decode(FORMAT)
   active_client.update({usrname:client})
   while connection:
      chat = client.recv(f_length).decode(FORMAT)
      if len(chat) == 0:
         pass
      elif chat[:7] == '!direct':
         new_chat = chat.split()
         reciever = new_chat[1]
         if reciever in active_client:
            num = 8+len(new_chat[1])
            direct_chat(reciever, chat[num:], usrname)
         if reciever not in active_client:
            client.send('[SERVER] Username does not exist'.encode(FORMAT))
      elif chat == '!disconnect':
         client.send('!disconnect'.encode(FORMAT))
         del active_client[usrname]
         break
      elif chat == '!online':
         print(f'Has respond from {usrname}: {chat} ')
         client.send(f'who on line is {[i for i in active_client]}'.encode(FORMAT))
      elif chat[:1] != '!':
         print(f'Has respond from {usrname}: {chat} ')
         chat_system(client, usrname, chat)



def direct_chat(usrname, chat, sender):
   active_client[usrname].send((f'[DIRECT CHAT] {sender}:' + chat).encode(FORMAT))
   print('Direct message sended')



def chat_system(client, usrname, chat):
   for i in (active_client):
      if i != usrname:
         new_chat = ('{:}: {:}'.format(usrname, chat))
         try:
            active_client[i].send(new_chat.encode(FORMAT))
            print(f'{usrname} has been sended {chat}')
         except ConnectionResetError:
            list_a.append(i)
   for i in list_a:
      del active_client[i]
   del list_a[:]

      
def launced():
   server.listen()
   while True:
      client,addr = server.accept()
      thread = threading.Thread(target=client_management, args=(client, addr))
      thread.start()
      print("")
      print(f'[ACTIVE CONNECTIONS] {threading.activeCount() - 1}')


print('[SERVER] is running')
launced()

