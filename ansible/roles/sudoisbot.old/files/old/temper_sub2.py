import zmq

# So that you can copy-and-paste this into an interactive session, I'm
# using threading, but obviously that's not what you'd use

# I'm the subscriber that multiple clients are writing to
def subscriber():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.setsockopt(zmq.SUBSCRIBE, b'name: ')
    # Even though I'm the subscriber, I'm allowed to get this party
    # started with `bind`
    socket.bind('tcp://127.0.0.1:5000')

    while True:
        data = socket.recv()
        print(data)

subscriber()
