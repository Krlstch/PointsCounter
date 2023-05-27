from server import server
import threading
import time

class Main:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.server = server.Server(self)

    def run_server(self):
        self.server.run()

def add(main):
    while True:
        time.sleep(1)
        main.score1 += 1
        time.sleep(1)
        main.score2 += 2

if __name__ == "__main__":
    main = Main()
    threading.Thread(target=add, args=(main,)).start()
    main.run_server()
