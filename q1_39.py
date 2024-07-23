# ~~~ This is a template for question 1  ~~~

#Imports:

###Part A###
#~~~  implementation of queue class  ~~~
class Queue:
    # Initializes a Queue object, default values for head and tail are None, and 0 for size.
    def __init__(self):
        self.head = None
        self.tail = None  
        self.q_size = 0   

    # Returns the value of the front element
    def front(self):
        if self.empty():
            raise IndexError("front() called on empty queue")
        return self.head.value

    # Checks if the queue is empty
    def empty(self):
        return self.q_size == 0

    def enqueue(self, x):
        # Add a new item to the end of the queue
        new_node = Node(x)
        if self.empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self.q_size += 1

    # Deletes the first item and return its value
    def dequeue(self):
        if self.empty():
            raise IndexError("dequeue() called on empty queue")
        value = self.head.value
        self.head = self.head.next
        self.q_size -= 1
        if self.empty():
            self.tail = None
        return value

# Represents a node in the Queue
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

###Part B###
def Was_an_attack(A=list,n=int,t=float):
    # Sorts the requests
    A = sorted(A, key=lambda x: (x[0].lower(), x[1]))
    q = Queue()
    # Iterates through the list of requests until either an attack is identified or all requests have been processed 
    for request, time in A:
        # Initializes variables for subsequent operations
        if q.empty():
            rqst = request.lower()
            mn = time
        else:
            rqst = q.front()[0].lower()
            mn = q.front()[1]
        # Determines the relevance of the current request
        if rqst == request.lower() and time - mn <= t:
            q.enqueue([request.lower(), time])
            # Verifies if enough requests have been accumulated to identify an attack
            if q.q_size == n:
                return [f"There was an attack on second {mn}",f"{mn}",f"{request}"]
        # Ensures comprehensive detection of all potential attacks
        elif rqst == request.lower() and time - mn > t:
            q.dequeue()
            mn = q.front()[1]
            while not q.empty():
                if time - mn > t:
                    q.dequeue()
                    mn = q.front()[1]
                else:
                    break
        # Empties the queue when a request is deemed irrelevant to ensure accurate subsequent checks
        else:
            while not q.empty():
                q.dequeue()
    return 0    # ['There was an attack on second str(XX)',XX,The attack word] ##XX - first second of the attack time

