import collections
import hashlib
import math
import random

from bitstring import BitArray
from math import log2

from simulation.data_handler import sorted_nodes_occur

class Server:
    def __init__(self, id, capacity=4):
        self.id = id
        self.capacity = capacity
        self.slots = set()
        self.left = self.right = None

    def insert(self, item_id, buffer=False):
        if item_id in self.slots:
            raise Exception("Item " + str(item_id) + " already in server!")
        elif len(self.slots) < self.capacity:
            self.slots.add(item_id)
            return True     # returns True if spot was found
        elif buffer:
            if len(self.slots) < self.capacity+1:
                self.slots.add(item_id)
                return True  # returns True if spot was found
        else:
            raise Exception("Trying to insert item " + str(item_id) + " in full server!")

    def get_current_occupation(self):
        return len(self.slots)

    def check_for_item(self, item_id):
        return item_id in self.slots

    def remove_item(self, item_id):
        if item_id in self.slots:
            self.slots.remove(item_id)
            return True
        return False

    def __str__(self):
        return str(self.id) + ", " + str(self.slots)

class CompleteTree:

    def __init__(self):
        self.server_capacity = 4
        self.most_sign_bit = -99

        self.root = None
        self.index2server = dict()
        self.bit_string2index = dict()
        self.initial_occupation = -99 # self.server_capacity/2
        self.random_seed = random.randint(0, 1000)

    def set_c(self, c):
        self.server_capacity = c
        self.initial_occupation = self.server_capacity / 2

    def set_c_set_f(self, c, f):
        """ Define f param (server's initial occupation) for simplicity """
        self.server_capacity = c
        self.initial_occupation = f

    def initialize_servers(self, n_items):
        """ Create tree-structure with needed servers.
            @param: number of distinct items which appear in the sequence """
        self.most_sign_bit = int(log2(n_items))+2            # determine depth of tree
        if self.server_capacity == 2:
            self.most_sign_bit = int(log2(n_items))+5
        elif self.server_capacity == 1:
            self.most_sign_bit = int(log2(n_items))+10
        n_servers = int(math.pow(2, self.most_sign_bit+1) - 1)
        for n in range(0,n_servers):
            parent = self.root
            if parent is None:

                # root is null, make this the new root, index == 0, done
                self.root = Server(id=0, capacity=self.server_capacity)
                self.index2server[self.root.id] = 0
                self.bit_string2index[0] = collections.deque()
            else:
                currIndex = len(self.index2server)
                if (currIndex % 2 == 0):  # right child
                    parentIndex = (currIndex - 2) / 2
                    bit = 1
                else:
                    parentIndex = (currIndex - 1) / 2  # left child
                    bit = 0
                newBitString = self.bit_string2index[parentIndex].copy()
                pathToConsume = newBitString.copy()
                parent = self.getParentOfInsertingNode(pathToConsume)

                #newNode = Node(newItem, currIndex)
                new_server = Server(id=currIndex, capacity=self.server_capacity)
                if bit == 1:
                    parent.right = new_server
                else:
                    parent.left = new_server
                newBitString.append(bit)
                self.bit_string2index[currIndex] = newBitString
                self.index2server[new_server.id] = currIndex

    def fill_for_optimal(self, sequence):
        """ sort items according to their frequency and add them to the tree """
        list_seq = []
        for r in sequence:
            list_seq.append(sequence[r])
        sorted = sorted_nodes_occur(list_seq)
        while sorted:
            self.insert(sorted.pop()[0])        # most freq items will be at end of list

    def get_hash(self, item_id):
        """Calculates hash on the fly"""
        if type(item_id) == int:
            return BitArray(hex=hashlib.sha512(str(int(item_id)+self.random_seed).encode()).hexdigest()).bin[:self.most_sign_bit]
        else:
            return BitArray(hex=hashlib.sha512(str(str(item_id)).encode()).hexdigest()).bin[
                   :self.most_sign_bit]

    #def get_hash_str(self, item_id):


    def insert(self, item_id):
        """Insert a new value in the tree. Takes one argument (the Item) """
        parent = self.root
        if parent.get_current_occupation() < self.initial_occupation:
            parent.insert(item_id)
        else:
            path = self.get_hash(item_id)
            for i in range(0, len(path)):
                step = path[i]
                if step == '1':       # 1 == left step
                    if not parent.left:        # if there is no server left on this path, add on the fly
                        currIndex = len(self.index2server)
                        new_server = Server(id=currIndex, capacity=self.server_capacity)
                        self.index2server[new_server.id] = currIndex
                        parent.left = new_server
                    if parent.left.get_current_occupation() < self.initial_occupation:
                        parent.left.insert(item_id)
                        return
                    else:
                        parent = parent.left
                elif step == '0':
                    if not parent.right:        # if there is no server left on this path, add on the fly
                        currIndex = len(self.index2server)
                        new_server = Server(id=currIndex, capacity=self.server_capacity)
                        self.index2server[new_server.id] = currIndex
                        parent.right = new_server
                    if parent.right.get_current_occupation() < self.initial_occupation:
                        parent.right.insert(item_id)
                        return
                    else:
                        parent = parent.right

    def getParentOfInsertingNode(self, path):
        currNode = self.root

        while path:
            if path.popleft() == 1:
                currNode = currNode.right
            else:
                currNode = currNode.left
        return currNode


    def getNodesInOrder(self):
        buf = collections.deque()
        root = self.root
        output = []
        final = []
        if not root:
            print("No root")
        else:
            buf.append(root)
            count, nextCount = 1, 0
            while count:
                node = buf.popleft()
                if node:
                    output.append(node)
                    count -= 1
                    for n in (node.left, node.right):
                        if n:
                            buf.append(n)
                            nextCount += 1
                        else:
                            buf.append(None)
                if not count:
                    final.append(output)
                    count, nextCount = nextCount, 0
        return output


def print_tree(root):
    print("Current Treestructure:")
    buf = collections.deque()
    output = []
    if not root:
        print("No root")
    else:
        buf.append(root)
        count, nextCount = 1, 0
        while count:
            node = buf.popleft()
            if node:
                #output.append(node.guest)
                for n in node.slots:
                    output.append(str(n))
                output.append("| ")
                count -= 1
                for n in (node.left, node.right):
                    if n:
                        buf.append(n)
                        nextCount += 1
                    else:
                        buf.append(None)
            # else:
            #   output.append('$')
            if not count:
                print(*output)
                output = []
                count, nextCount = nextCount, 0
