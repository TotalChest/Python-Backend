#!/usr/bin/env python
from time import time
import configparser
import argparse
import socket
import logging
import wikipedia


class Config():
    def __init__(self, config_path):
        config = configparser.ConfigParser()
        config.read(config_path)

        self.port = int(config['DEFAULT']['port'])
        self.log_file = config['DEFAULT']['log_file']
        self.mode = config['DEFAULT']['mode']
        self.timeout = int(config['DEFAULT']['timeout'])
        self.max_connections = int(config['DEFAULT']['max_connections'])
import argparse


def get_logger(log_file):
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger


def make_response(data):
    try:
        data = data.split('&')
        data = dict(map(lambda x: x.split('='), data))
    except ValueError:
        logger.error('Bab request: wrong format')
        return 'Bab request: wrong format'
    if 'format' in data and 'q' in data:
        return str({i:entity for i, entity in
                    enumerate(wikipedia.search(data['q']))})
    else:
        logger.error('Bab request: no "format" or "q" arguments')
        return 'Bab request: no "format" or "q" arguments'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='configuration file')

    args = parser.parse_args()
    config = Config(args.config_file)
    logger = get_logger(config.log_file)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', config.port))
    sock.settimeout(config.timeout)

    sock.listen()
    while config.max_connections:
        config.max_connections -= 1

        conn, addr = sock.accept()
        print('connected:', addr)

        # request
        start_time = time()
        request = ''
        data = conn.recv(1024)
        request = data.decode('utf-8')

        # response
        response = make_response(request)
        conn.send(response.encode('utf-8'))

        all_time = time() - start_time
        logger.info(f'time: {all_time}, size: {len(request)}')

        conn.close()