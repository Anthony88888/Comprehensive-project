import selectors
import threading
import socket
import time


selector = selectors.DefaultSelector()

sock = socket.socket()
sock.bind(('127.0.0.1', 8080))
sock.listen()
print(1, sock)
print(2, sock.fileno())
sock.setblocking(False)


def accept(sock:socket.socket, mask):
    conn, raddr = sock.accept()
    conn.setblocking(False)
    print(3, conn)

key = selector.register()

selector.register()
selector.unregister()
selector.select()
selector.close()
selector.fileno()
selector.get_key()
selector.get_map()

