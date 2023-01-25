import socket
import pickle
import db_ops as db
import struct

def check_type(data):
    if type(data) == type(list()):
            return 1
    if type(data) == type(dict()):
            return 2

def fetch_data():
    hw_recv = list()
    pkg_recv = dict()
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("[SERVER] Socket created successfully")
    port = 25000
    s.bind(('', port))
    print(f"[SERVER] Socket bound to port {port}")
    s.listen(5)
    print("[SERVER] Socket listen mode ON")

    while True:
        c, addr = s.accept()

        data_size = struct.unpack('>I', c.recv(4))[0]
        payload = b""
        remaining_payload_size = data_size
        while remaining_payload_size != 0:
            payload += c.recv(remaining_payload_size)
            remaining_payload_size = data_size - len(payload)

        temp = pickle.loads(payload)
        if check_type(temp) == 1:
            hw_recv = temp
        elif check_type(temp) == 2:
            pkg_recv = temp
        c.send("SUCCESS".encode())

        data_size = struct.unpack('>I', c.recv(4))[0]
        payload = b""
        remaining_payload_size = data_size
        while remaining_payload_size != 0:
            payload += c.recv(remaining_payload_size)
            remaining_payload_size = data_size - len(payload)

        temp = pickle.loads(payload)
        if check_type(temp) == 1:
            hw_recv = temp
        elif check_type(temp) == 2:
            pkg_recv = temp

        c.send("SUCCESS".encode())
        c.close()
        break
    data = list()
    data.append(hw_recv)
    data.append(pkg_recv)
    return data


def runserver():
    hw_data = list()
    pkg_data = dict()
    received = fetch_data()
    hw_data = received[0]
    pkg_data = received[1]
    db.db_conn("hwinfo.db", hw_data, pkg_data)


if __name__ == "__main__":
    while True:
        runserver()