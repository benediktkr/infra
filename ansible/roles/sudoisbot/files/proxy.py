#!/usr/bin/python3 -u

import os

import zmq

def proxy():
    context = zmq.Context()

    # facing publishers
    frontend_addr = os.environ["ZMQ_FRONTEND"]
    frontend = context.socket(zmq.XSUB)
    frontend.bind(frontend_addr)

    # facing services (sinks/subsribers)
    backend_addr = os.environ["ZMQ_BACKEND"]
    backend = context.socket(zmq.XPUB)
    backend.bind(backend_addr)

    print(f"Starting zmq proxy({frontend_addr}, {backend_addr})")
    zmq.proxy(frontend, backend)

    # we never get here
    frontend.close()
    backend.close()
    context.close()

if __name__ == "__main__":
    proxy()
