import socket
import threading
from threading import Thread
from colored import fg, bg, attr

color1 = fg('green')
color2 = fg('red')
color3 = fg('yellow')
reset = attr('reset')

try:
	file1 = open('client.txt', 'r')
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

username = input(color1 + '\nEnter a username : ' + reset)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port)) 


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if (message == 'USERNAME'):
                client.send(username.encode('utf-8'))
            else:
                print(color1 + message + reset)

        except:
            print(color2 + 'An error occurred!!!' + reset)
            client.close()
            break

def write():
    while True:
        message = f'\n{username}: {input("")}\n'
        client.send(message.encode('utf-8'))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

print('\n')
