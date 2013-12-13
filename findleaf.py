
import psycopg2
import sys
import bcrypt
import RPi.GPIO as GPIO
import time

username = sys.argv[1]
password = sys.argv[2]
branchname = sys.argv[3]
leafname = sys.argv[4]

hashed = '$2a$10$MBMUptwhBwet1LOCzieokunvHaYvsZJzrIh0o0rlonkGqZYXKqVOe'

ex = "host=192.168.1.3 user=%s password=%s  dbname=insite-web_development" % (username, password)
conn = psycopg2.connect(ex)
cur = conn.cursor()

ex = "select encrypted_password from users where username = '%s'" % username
cur.execute("select encrypted_password from users where username = 'ken'")
prevhashtuple = cur.fetchone()
prevhash = prevhashtuple[0]

if prevhash == hashed:
	print "You have successfully connected"
else:
	print "Incorrect password or login info"

ex = "select user_id from branches where name = '%s';" % branchname
cur.execute(ex)
useridtuple = cur.fetchone()
userid = useridtuple[0]

ex = "select id from branches where name = '%s';" % branchname
cur.execute(ex)
branchidtuple = cur.fetchone()
branchid = branchidtuple[0]

ex = "select id from leafs where name = '%s';" % leafname
cur.execute(ex)
leafidtuple = cur.fetchone()
leafid = leafidtuple[0]

leaf_db_id = str(leafname) + '_' + str(userid) + str(branchid) + str(leafid)

ex = "host=192.168.1.3 user=postgres password=%s  dbname=leaf_db" % password

conn = psycopg2.connect(ex)
cur = conn.cursor()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.output(18, GPIO.HIGH)
#while GPIO.input(17):
#       pass
GPIO.output(18, GPIO.LOW)
GPIO.output(25, GPIO.HIGH)

button_pressed = False
measurement_wait=3


while True:
        time_1 = time.time()
        tfile = open("/sys/bus/w1/devices/28-000004e85d00/w1_slave")
        text = tfile.read()
        tfile.close()
        temperature_data = text.split()[-1]
        temperature = float(temperature_data[2:])
        temperature = temperature / 1000
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        insert = "INSERT INTO %s (time, %s) VALUES(%s, %s);" %(leaf_db_id, leafname , '%s', '%s')
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
#       if button_pressed:
#               break

GPIO.output(25, GPIO.LOW)
