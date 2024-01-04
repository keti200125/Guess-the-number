import socket
import selectors
import requests


class Server:
    def __init__(self, host: str, port: int):
        self.selector = selectors.DefaultSelector()
        self.host = host
        self.port = port

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        sock.setblocking(False)
        self.selector.register(sock, selectors.EVENT_READ, self.__add_socket_to_selector) 
    
    def __add_socket_to_selector(self, key):
        sock = key.fileobj
        connection, address = sock.accept()
        connection.setblocking(False)
        print('Connected to host: {} port: {}'.format(address[0], address[1]))
        self.selector.register(connection, selectors.EVENT_READ | selectors.EVENT_WRITE, self.__handle_client_query)

    def __get_subject_and_number_fact(self, input_str: str):
        number = input_str.split(' ', 1)[0]
        subject = input_str.split(' ', 1)[1]
        query = "http://numbersapi.com/" + number + subject
        data = requests.get(query)
        responce = data.text
        chunked = responce.split(' ')
        if '/' in number:
            chunked[1] = '*'
        else:
            chunked[0] = '*'
        return ' '.join(chunked)

    def __handle_client_query(self, key: selectors.SelectorKey):
        try:
            current_socket = key.fileobj
            recieved_info = current_socket.recv(1024)
            if recieved_info:
                data = recieved_info.decode()
                fact = self.__get_subject_and_number_fact(data)
                current_socket.sendall(fact.encode())
            else:
                print("Client disconnected")
                self.selector.unregister(current_socket)
                current_socket.close()
        except BlockingIOError:
            pass

    def start(self):
        try:
            print("Server is up and running on host {} and port {}".format(self.host, self.port))
            while True:
                evn = self.selector.select(timeout=None)
                for key, _ in evn:
                    callback = key.data
                    callback(key)
        except KeyboardInterrupt:
            print("Caught keyboard interrupt, exiting")

    def __del__(self):
        self.selector.close()

s = Server("127.0.0.1", 33333)
s.start()