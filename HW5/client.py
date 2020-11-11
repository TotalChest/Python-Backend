#!/usr/bin/env python
import socket
import argparse


sock = socket.socket()
sock.connect(('127.0.0.1', 9111))

parser = argparse.ArgumentParser()
parser.add_argument('request', help='arguments for request')
args = parser.parse_args()
request = args.request

sock.sendall(request.encode('utf-8'))
data = sock.recv(1024)
sock.close()

print(data.decode('utf-8'))
