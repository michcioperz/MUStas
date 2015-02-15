#!/usr/bin/env python2
from dunnohowtnameit.app import start
from argparse import ArgumentParser
import logging


parser = ArgumentParser()
parser.add_argument('-b', '--bind', '--host', type=str, default='127.0.0.1')
parser.add_argument('-p', '--port', type=int, default=7999)
parser.add_argument('-l', '--log', type=str, default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
args = parser.parse_args()
start(host=args.bind, port=args.port, loglevel=getattr(logging, args.log, logging.INFO))
