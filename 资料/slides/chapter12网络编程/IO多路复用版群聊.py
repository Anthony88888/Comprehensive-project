
import threading
import selectors
import socket
import time
import datetime


class ChatServer:
    def __init__(self, ip='127.0.0.1', port=9999):
        self.sock = socket.socket()
        self.addr = ip, port

        self.event = threading.Event()
        #self.lock = threading.Lock()
        self.selector = selectors.DefaultSelector()


    def start(self):
        self.sock.bind(self.addr)
        self.sock.listen() # listen 参数可以写，可以不写
        self.sock.setblocking(False)

        #threading.Thread(target=self.accept, name='accept').start()
        self.selector.register(self.sock, selectors.EVENT_READ, self.accept)

        #self._select()
        threading.Thread(target=self._select, name='selector', daemon=True).start()

    def _select(self):

        while not self.event.is_set():
            events = self.selector.select() # [(key, mask)]
            print('-' * 30)
            for key, mask in events: # 你让我盯住的某一个对象的某几个事件发生了
                time.sleep(1)
                print(1, key)
                print(2, key.fileobj)
                print(3, key.data)
                key.data(key.fileobj)

    def accept(self, s:socket.socket):
        sock, caddr = s.accept()
        sock.setblocking(False)


        #threading.Thread(target=self.recv, name='recv', args=(sock, caddr)).start()
        self.selector.register(sock, selectors.EVENT_READ, self.recv)

    def recv(self, sock:socket.socket):
        caddr = sock.getpeername()
        try:
            data = sock.recv(1024)  # bytes
        except:
            data = b'quit'

        data = data.rstrip()
        print(type(data), data, "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if data == b'quit' or data == b'': # 线程安全

            self.selector.unregister(sock)
            sock.close()
            print('{} bye'.format(sock))
            return

        msg = '{} {}:{} {}'.format(datetime.datetime.now(), *caddr, data).encode()

        # for s in self.clients.values():
        #     s.send(msg)
        for key in self.selector.get_map().values():
            print('+++++++++++++++++++++++++')
            print(self.recv) # 绑定
            print(key.data) # 是否一致
            print(self.recv is key.data)
            print(self.recv == key.data)
            if key.data == self.recv:
                key.fileobj.send(msg)

    def stop(self):
        self.event.set()
        fs = []
        for fd, key in self.selector.get_map().items():
            fs.append(key.fileobj)
        for f in fs:
            self.selector.unregister(f)
            f.close()
        self.selector.close()


cs = ChatServer()
cs.start()

while True:
    cmd = input('>>')
    if cmd.strip() == 'quit':
        cs.stop()
        break

    print(threading.enumerate())
    print(list(cs.selector.get_map().keys()))
