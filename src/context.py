import sys
from socket import socket, AF_INET, SOCK_STREAM
from contextlib import suppress


def context(obj, handler_callback):

    ctx = obj.__enter__()
    try:
        handler_callback(ctx)
    finally:
        exc_type, exc_val, exc_tb = sys.exc_info()
        obj.__exit__(exc_type, exc_val, exc_tb)


class LazyConnection:

    def __init__(self, address, family=AF_INET, sock_type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.sock_type = sock_type
        self.sock = None
    
    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError('You already connected!')
        self.sock = socket(family=self.family=, type=self.sock_type)
        self.sock.connect(self.address)
        return self.sock
    
    def __exit__(self, exc_type, exc_val, tb):
        try:
            self.sock.close()
        finally:
            self.sock = None


class ConnectionFactory:

    def __init__(self, *, maxsize=50, address, family=AF_INET, sock_type=SOCK_STREAM):
        self.__maxsize = 50
        self.__address = address
        self.__family = family
        self.__sock_type = sock_type
        self.__connections = []
    
    def __enter__(self):
        if len(self.__connections) < self.__maxsize:
            new_connection = LazyConnection(address, family, sock_type)
            self.__connections.append(new_connection)
            return new_connection
    
    def __exit__(self, exc_type, exc_val, tb):
        self.__connections.pop().__exit__(exc_type, exc_val, tb)