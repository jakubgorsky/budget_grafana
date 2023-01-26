import subprocess
import re
import socket
import pickle
import struct

# fetch system and hardware info
uname = subprocess.run(['uname', '-sr'],
			stdout=subprocess.PIPE).stdout.decode('ascii')
hw = subprocess.run(['sudo', 'lshw', '-short'],
                    stdout=subprocess.PIPE).stdout.decode('ascii')
hardware_data = list()
hardware_data.append(uname)
for l in hw.splitlines():
	hardware_data.append(re.sub(r'\s+', ' ', l))

# fetch package data
package_data = dict()
pkg = subprocess.run(['pacman', '-Qe'],
			stdout=subprocess.PIPE).stdout.decode('ascii')
for p in pkg.splitlines():
	package_data[p.split()[0]] = p.split()[1]


s = socket.socket()
port = 25000
ip_addr = '127.0.0.1'
s.connect((ip_addr, port))

pkg_dat = pickle.dumps(package_data)
s.sendall(struct.pack('>I', len(pkg_dat)))
s.sendall(pkg_dat)

recv_msg = s.recv(1024).decode()

hw_data = pickle.dumps(hardware_data)
s.sendall(struct.pack('>I', len(hw_data)))
s.sendall(hw_data)

recv_msg = s.recv(1024).decode()

print(recv_msg)

s.close()