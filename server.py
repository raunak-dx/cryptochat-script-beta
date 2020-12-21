import sys
import threading
import socket
from colored import fg, bg, attr

color1 = fg('green')
color2 = fg('red')
color3 = fg('yellow')
reset = attr('reset')

try:
	file1 = open('server.txt', 'r')
	print(' ')
	print (color3 + file1.read() + reset)
	file1.close()
except IOError:
	print('\nBanner File not found!')


host = input(color1 + '\nEnter server IP: ' + reset)
print('\n')
port = int(input(color1 + 'Enter TCP port no.: ' + reset))
print('\n')

#host = '127.0.0.1'
#port = 64352

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
usernames = []


def broadcast(message): 
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
            msg = message.decode('utf-8')
            print(color1 + msg + reset)
            msglow = msg.lower()
            l = len(msglow)
            trigger = msglow.find('exit',0,l)
            if trigger >= 0:
                index = clients.index(client)
                username = usernames[index]
                broadcast(f'\n{username} left the chat!!!\n'.encode('utf-8'))
                print(color2 + f'\n{username} left the chat!!!\n' + reset)
                usernames.remove(username)
                clients.remove(client)
                client.close()
                break

        except:
           index = clients.index(client)
           username = usernames[index]
           broadcast(f'\n{username} left the chat!!!\n'.encode('utf-8'))
           print(color2 + f'\n{username} left the chat!!!\n' + reset)
           usernames.remove(username)
           clients.remove(client)
           client.close()
           break


def receive():
    while True:
        client, address = server.accept()
        print(color1 + f'Connected with {str(address)}!!!' + reset)

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(color1 + f'Username of the client is: {username}!!!\n' + reset)
        client.send('Connected to the server!!!\n'.encode('utf-8'))
        broadcast(f'\n{username} joined the chat!!!\n'.encode('utf-8'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print(color1 + '\nWelcome to the server!!!\n' + reset)
print(color1 + '\nServer is active and listening......!!!\n' + reset)
receive()
