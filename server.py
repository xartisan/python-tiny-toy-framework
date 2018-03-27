import socket
from utils import log
import threading
from request import Request
from routes import router


def handle_request(connection, address):
    received_bytes = connection.recv(4096)
    http_text = received_bytes.decode('utf-8')

    if len(http_text.split()) < 2:
        connection.close()
        return

    request = Request.from_http_and_address(http_text, address)
    log('Request is {}'.format(request))
    log('Request path is {}'.format(request.path))

    response = router.handle(request)
    # log('Response:\n' + response.decode('utf-8'))
    log('response is', response)
    connection.sendall(response)
    connection.close()


def run(host, port):
    log('start at {}{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen(5)
        while True:
            connection, address = s.accept()
            threading.Thread(target=handle_request, args=(connection, address)).start()


if __name__ == '__main__':
    config = {
        'host': '',
        'port': 8000,
    }
    run(**config)
