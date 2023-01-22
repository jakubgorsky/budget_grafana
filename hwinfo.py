import subprocess
import re
import sqlite3

data = ["", list(),dict()]
pkg = "pacman -Qe"
data[0] = subprocess.run(['uname', '-sr'],
			stdout=subprocess.PIPE).stdout.decode('ascii')

hw = subprocess.run(['sudo', 'lshw', '-short'],
                    stdout=subprocess.PIPE).stdout.decode('ascii')

for l in hw.splitlines():
	data[1].append(re.sub(r'\s+', ' ', l))

pkg = subprocess.run(['pacman', '-Qe'],
			stdout=subprocess.PIPE).stdout.decode('ascii')
for p in pkg.splitlines():
	data[2][p.split()[0]] = p.split()[1]

conn = sqlite3.connect('hwinfo.db')

c = conn.cursor()
try:
	c.execute("""CREATE TABLE packages (
				name text,
				version text
				)""")
except:
    print("Table packages already exists")

try:
    c.execute("""CREATE TABLE hwinfo (
     			element text
        		)""")
except:
    print("Table hwinfo already exists")

c.execute("SELECT * FROM packages")
result = c.fetchall()

if len(result) == 0:
    for key in data[2].keys():
        c.execute(f"INSERT INTO packages VALUES ('{key}', '{data[2][key]}')")
        print(f"[DB-LOG] Successfully inserted '{key}: {data[2][key]}' into table 'packages'")
else:
    c.execute("SELECT * FROM packages")
    for key in data[2].keys():
        result = c.fetchone()
        if type(result) is type(None):
            continue
        if key != result[0]:
            c.execute(f"INSERT INTO packages VALUES ('{key}', '{data[2][key]}')")
            print(f"[DB-LOG] Successfully inserted '{key}: {data[2][key]}' into table 'packages'")


c.execute("SELECT * FROM hwinfo")
result = c.fetchall()

if len(result) == 0:
    for item in data[1]:
        c.execute(f"INSERT INTO hwinfo VALUES ('{item}')")
        print(f"[DB-LOG] Successfully inserted '{item}' into table 'hwinfo'")
else:
    c.execute("SELECT * FROM hwinfo")
    for item in data[1]:
        result = c.fetchone()
        if type(result) is type(None):
            continue
        if item != result[0]:
            c.execute(f"INSERT INTO hwinfo VALUES ('{item}')")
            print(f"[DB-LOG] Successfully inserted '{item}' into table 'hwinfo'")

c.execute(f"SELECT * FROM hwinfo WHERE element='System: {data[0]}'")
result = c.fetchall()
if len(result) == 0:
    c.execute(f"INSERT INTO hwinfo VALUES ('System: {data[0]}')")
    print(f"[DB-LOG] Successfully inserted '{data[0]}' into table 'hwinfo'")

conn.commit()
conn.close()
