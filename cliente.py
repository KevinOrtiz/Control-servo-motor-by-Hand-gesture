import socket               

s = socket.socket()        
host = '192.168.137.185'# ip of raspberry pi 
port = 8080               
s.connect((host, port))
valor1 = '2.5'
s.send(valor1)
s.close()