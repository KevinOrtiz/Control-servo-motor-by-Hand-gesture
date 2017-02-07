import socket
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
frequencyHertz = 50
s = socket.socket()
host = '192.168.137.185'
port = 8080
pwm  = GPIO.PWM(11, frequencyHertz)
leftPosition  = 0.75
rightPosition = 2.5
middlePosition = (rightPosition -leftPosition) / 2 + leftPosition
positionList   = [leftPosition, middlePosition, rightPosition, middlePosition]
msPerCycle     = 1000/frequencyHertz
s.bind((host,port))

s.listen(5)
while True:
	c, addr = s.accept()
	print ('obtener conexion de', addr)
	c.send('Gracias por tu conecxion')
	data = c.recv(1024)
	print data
	for i in range(3):
		for position in positionList:
			dutyCyclePercentage = float(data) * 100 / msPerCycle
			print "Position" + str(position)
			print "Duty Cycle" + str(dutyCyclePercentage) + "%"
			print ""
			pwm.start(dutyCyclePercentage)
			time.sleep(.5)
	GPIO.cleanup()
	pwm.stop()
	c.close()