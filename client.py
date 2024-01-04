import socket
import random


class TextColor:
    GREEN = '\033[32m'
    DEFAULT = '\033[0m'
    RED = '\033[31m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'

class Client:
    def __init__(self, server_host: str, server_port: int, username: str, subject: str, lo: int, hi: int,helper: bool, debug: bool):
        self.m_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_host = server_host
        self.server_port = server_port
        self.username = username
        self.subject = subject
        self.lo = lo
        self.hi = hi
        self.helper = helper
        self.debug = debug
    
    def __connect(self):
        try:
            self.m_socket.connect((self.server_host, self.server_port))
            print("Connection successful!")
        except ConnectionRefusedError as e:
            print("Connection error: {}".format(e))

    def __start_guessing(self, number, debug):
        str_number = str(number)
        if(debug):
            print("{}Psst number is {}{}".format(TextColor.RED, str_number, TextColor.DEFAULT))
        while True:
            print("{}Can you guess the number? If you don't like it write q.{}".format(TextColor.GREEN, TextColor.DEFAULT))
            num = input()
            if num == "q":
                break
            if int(num) == number:
                print("{}You just did it!!!{}".format(TextColor.BOLD, TextColor.DEFAULT))
                print("{}GOOD JOB, {}!!!{}".format(TextColor.BOLD, self.username ,TextColor.DEFAULT))
                print('\n')
                break
            elif int(num) > number and self.helper == True:
                print("You might try again. The number is smaller :(")
            elif int(num) < number and self.helper == True:
                print("You might try again. The number is greater :(")
            else:
                print("You might try again :(")

    def __start_round(self):
        print("{}Hello there {}. Get ready for your next question...".format(TextColor.YELLOW, self.username))
        number = random.randint(self.lo, self.hi)
        numberMonth = random.randint(self.lo,12)
        print("I just chose a random number between {} and {}. Here is a fact for it: {}".format(self.lo, self.hi, TextColor.DEFAULT))
        data = str(number) + ' ' + self.subject
        if self.subject == '/date':
             data = str(numberMonth) +'/' + str(number)  + ' ' + self.subject
        self.m_socket.sendall(data.encode())
        fact = self.m_socket.recv(1024)
        print(fact.decode())
        self.__start_guessing(number, self.debug)

    def start(self):
        self.__connect()

        while True:
            self.__start_round()
    
    def __del__(self):
        self.m_socket.close()

def start_game():
    helper = False
    subject = ''
    high = 10
    low = 1
    user = input("Enter your username: ")
    subjectInput= input("Choose subject(random, math, date): " )
    if subjectInput != 'date':
       level = input("Choose level(easy, medium, hard): ")
       if level == 'medium':
        high = 100
       elif level == 'hard':
        high = 800
    helperStr = input("Decide if you need help or not(yes, no): ")
    if helperStr == 'yes':
        helper = True
    if subjectInput == 'math':
        subject = '/math'
    elif subjectInput == 'date':
        subject = '/date'
        high = 28
    cl = Client("127.0.0.1", 33333, user,subject, low, high, helper, False)
    cl.start()    
start_game()