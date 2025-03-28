import os
import pickle

class Queue:
    def __init__(self, output_dir):
        self.items = []
        self.completed = CompletedList(output_dir)
        self.output_dir = output_dir

        pickled_queue = os.path.join(output_dir, "queue.pkl")
        if os.path.exists(pickled_queue):
            self.load()

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        if item not in self.items and item not in self.completed.items:
            if item.startswith("http") and ('mobilehealthconsumer.com' in item or 'angulartest' in item):
                self.items.insert(0,item)
                self.save()

    def dequeue(self):
        self.completed.add(self.items[-1])
        id_num = self.completed.size()
        return self.items.pop(), id_num

    def size(self):
        return len(self.items)

    def save(self):
        pickled_queue = os.path.join(self.output_dir, "queue.pkl")
        with open(pickled_queue, 'wb') as f:
            pickle.dump(self.items, f)

    def load(self):
        pickled_queue = os.path.join(self.output_dir, "queue.pkl")
        with open(pickled_queue, 'rb') as f:
            self.items = pickle.load(f)

    def __str__(self):
        return str(self.items)


class CompletedList:
    def __init__(self, output_dir):
        self.items = []
        self.output_dir = output_dir

        pickled_list = os.path.join(output_dir, "completed_list.pkl")
        if os.path.exists(pickled_list):
            self.load()

    def add(self, item):
        self.items.append(item)
        self.save()

    def size(self):
        return len(self.items)

    def save(self):
        pickled_list = os.path.join(self.output_dir, "completed_list.pkl")
        with open(pickled_list, 'wb') as f:
            pickle.dump(self.items, f)

    def load(self):
        pickled_list = os.path.join(self.output_dir, "completed_list.pkl")
        with open(pickled_list, 'rb') as f:
            self.items = pickle.load(f)

    def __str__(self):
        return str(self.items)

def clear():
    if os.path.exists('queue.pkl'):
        os.remove('queue.pkl')
    if os.path.exists('completed_list.pkl'):
        os.remove('completed_list.pkl')
