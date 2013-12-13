
import psycopg2
import RPi.GPIO as GPIO
import time
import sys

username = sys.argv[1]

password = sys.argv[2]
tablename = sys.argv[3]
#branchname = sys.argv[3]
#leafname = sys.argv[4]

ex = "host=192.168.1.3 user=%s password=%s  dbname=leaf_db" % (username, password)
print ex

conn = psycopg2.connect(ex)
cur = conn.cursor()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
#while GPIO.input(17):
#	pass
GPIO.output(18, GPIO.LOW)
GPIO.output(25, GPIO.HIGH)

button_pressed = False
measurement_wait=3

ex = "create table %s(time timestamp, temp numeric);" % tablename
cur.execute(ex)

ex= "INSERT INTO %s (time, temp)" % tablename
print ex

ex1= ex + 'VALUES(%s,%s);'
print ex1

while True:
	time_1 = time.time()
	tfile = open("/sys/bus/w1/devices/28-000004e85d00/w1_slave")
	text = tfile.read()
	tfile.close()
	temperature_data = text.split()[-1]
	temperature = float(temperature_data[2:])
	temperature = temperature / 1000
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	#timevars = (%s, %s) % timestamp temperature
	insert = "INSERT INTO %s (time, temp) VALUES(%s, %s);" %(tablename, '%s', '%s')
	print insert
	data = (timestamp, temperature) 
	print data
	cur.execute(insert, data)
	conn.commit()
	time_2 = time.time()	
	if(time_2 - time_1) < measurement_wait:
		no_of_sleeps = int(round((measurement_wait - (time_2 - time_1)) / 0.1))
		for i in range(no_of_sleeps):
			time.sleep(0.1)
			if GPIO.input(17):
				button_pressed = True
				break
#	if button_pressed:
#		break

GPIO.output(25, GPIO.LOW)
