"""
HTTP client simulator. It simulate a number of concurrent users and calculate the response time for each request.
"""
#python http_client.py http://192.168.56.101:31761/k8stb.webapp/function 100 1
#python http_client.py http://192.168.56.101:31761/k8stb.webapp/query?recordsCount=50000 10 1
import requests
import time
import threading
import sys

if len(sys.argv) < 4:
    print('To few arguments; you need to specify 3 arguments.')
    print('Default values will be used for server_ip, no of users and think time.\n')
    address = 'http://192.168.56.101:8080/k8stb.webapp/function/'  # ip address of the Swarm master node
    no_users = 1  # number of concurrent users sending request to the server
    think_time = 1  # the user think time (seconds) in between consequent requests
else:
    print('Default values have be overwritten.')
    address = sys.argv[1]
    no_users = int(sys.argv[2])
    think_time = float(sys.argv[3])


class MyThread(threading.Thread):
    def __init__(self, name, counter):
        threading.Thread.__init__(self)
        self.threadID = counter
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name + str(self.counter))
        workload(self.name + str(self.counter))


def workload(user):
    while True:
        t0 = time.time()
        requests.get(address)
        t1 = time.time()
        time.sleep(think_time)
        print("Response Time for " + user + " = " + str(t1 - t0))


if __name__ == "__main__":
    threads = []
    for i in range(no_users):
        threads.append(MyThread("User", i))

    for i in range(no_users):
        threads[i].start()

    for i in range(no_users):
        threads[i].join()