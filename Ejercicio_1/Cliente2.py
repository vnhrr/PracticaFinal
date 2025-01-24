import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5010))
mens = "Hola servidor soy cliente 2"
s.send(mens.encode())