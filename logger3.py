import psycopg2
import RPi.GPIO as GPIO
import time


conn = psycopg2.connect("host=192.168.1.3 user=postgres")
cur = conn.cursor()

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

GPIO.output(18, GPIO.HIGH)

while GPIO.input(17):
	pass

GPIO.output(18, GPIO.LOW)
GPIO.output(25, GPIO.HIGH)

datafile = open("temperaturedatalog", "w")

measurement_wait=5
button_pressed = False

while True:
	time_1 = time.time()
	tfile = open("/sys/bus/w1/devices/28-000004e85d00/w1_slave")
	text = tfile.read()
	tfile.close()
	temperature_data = text.split()[-1]
	temperature = float(temperature_data[2:])
	temperature = temperature / 1000
	timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
	cur.execute("""INSERT INTO finaltest(time, temp) VALUES(%s, %s);""",(timestamp, temperature))
	conn.commit()
	time_2 = time.time()	
	if(time_2 - time_1) < measurement_wait:
		no_of_sleeps = int(round((measurement_wait - (time_2 - time_1)) / 0.1))
		for i in range(no_of_sleeps):
			time.sleep(0.1)
			if GPIO.input(17):
				button_pressed = True
				break
	if button_pressed:
		break

datafile.close()
GPIO.output(25, GPIO.LOW)
