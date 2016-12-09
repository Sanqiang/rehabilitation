# from queue import Queue
import Queue


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def printBFS(node):
    q = Queue.Queue()
    q.put(node)

    while not q.empty():
        temp = q.get()
        if temp is not None:
            print(temp.value)
        else:
            print("NULL")
            continue
        if temp.left is not None:
            q.put(temp.left)
        else:
            q.put(None)
        if temp.right is not None:
            q.put(temp.right)
        else:
            q.put(None)

position1 = Node(3)
position2 = Node(9)
position3 = Node(20)
position6 = Node(1)
position7 = Node(5)
position1.left = position2
position1.right = position3
position3.left = position6
position3.right = position7
printBFS(position1)

