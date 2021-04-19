
from threading import Semaphore

class ProductConsumer:
    def __init__(self):
        self.queue = []
        self.isEmpty = Semaphore(0)
        self.isFull = Semaphore(0)
    
    def put(self, item):
        if len(self.queue) == 10:
            self.isFull.acquire()
        self.queue.append(item)
        self.isEmpty.release()
    
    def get(self):
        self.isEmpty.acquire()
        item = self.queue.pop(0)
        self.isFull.release()
        return item
