import socket
import RPi.GPIO as GPIO  #importamos la librerias
import time
GPIO.setmode(GPIO.BOARD) #raspberry en modo Board
GPIO.setup(11, GPIO.OUT) #pin 11 como salida 
GPIO.setup(13, GPIO.OUT)  #pint 13 como salida 
frequencyHertz = 50
s = socket.socket()
host = '192.168.137.241'
port = 8080
#pwm  = GPIO.PWM(11, frequencyHertz)
p = GPIO.PWM(11,frequencyHertz)
p.start(7.5)
servo2 = GPIO.PWM(13,frequencyHertz)
servo2.start(7.5)

s.bind((host,port))
print 'hola'
s.listen(5)
try:
	while True:  #loop infinito
		c, addr = s.accept()
		print ('obtener conexion de', addr)
		c.send('Gracias por tu conecxion')
		data = c.recv(1024)
		print data
		if (data == 'servo1Izq'):
			p.ChangeDutyCycle(4.5) #enviamos un pulso 4.5% para girar servo a la izquierda
			time.sleep(0.5)
		if (data == 'servo1Dere'):
			p.ChangeDutyCycle(10.5) #girar servo a la derecha
			time.sleep(0.5)
		if (data == 'servo1Centro'):	
			p.ChangeDutyCycle(7.5) #centrar servo 
			time.sleep(0.5)
			
		if (data == 'servo2Izq'):
			servo2.ChangeDutyCycle(4.5) #enviamos un pulso 4.5% para girar servo a la izquierda
			time.sleep(0.5)
		if (data == 'servo2Dere'):
			servo2.ChangeDutyCycle(10.5) #girar servo a la derecha
			time.sleep(0.5)
		if (data == 'servo2Centro'):
			servo2.ChangeDutyCycle(7.5) #centrar servo 
			time.sleep(0.5)
except KeyboardInterrupt:	
	p.stop()
	GPIO.cleanup()
	c.close()
	