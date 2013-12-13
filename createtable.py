
import sys
import psycopg2

username = sys.argv[1]
password = sys.argv[2]
tablename = sys.argv[3]

ex = "host=192.168.1.3 user=%s password=%s  dbname=leaf_db" % (username, password)
print ex

conn = psycopg2.connect(ex)
cur = conn.cursor()

ex = "create table %s(time timestamp, temp numeric);" % tablename
cur.execute(ex)
