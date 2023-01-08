from pushdown.treeStructure import *


class static_offline():

    def __init__(self, tree):
        self.tree = tree
        self.debug = False
        self.swaps = 0
        self.adjust_cost = 0
        self.access_cost = 0
        self.n_accesses = 0

    # for testing
    def reset(self):
        self.swaps = 0
        self.adjust_cost = 0
        self.access_cost = 0

    def access(self, item_id):
        self.n_accesses += 1
        if self.debug:
            print("\nRandom Push-Access " + str(item_id))

        if not self.find(item_id):
            raise Exception("No Item for " + str(item_id) + " found")
        else:
            if self.debug:
                print_tree(self.tree.root)

    def find(self, id):
        parent = self.tree.root
        path = self.tree.get_hash(id)
        if parent.check_for_item(id):      # root access
            return True
        else:
            for i in range(0, len(path)):
                if not path[i]:
                    raise Exception("No step left in path!")
                elif path[i] == '1':  # left step
                    if parent.left.check_for_item(id):
                        if self.debug:
                            print("Found item on depth " + str(i+1))    # depth + 1 because first step brings to dp=1
                        self.access_cost += 1
                        return True
                    else:
                        parent = parent.left
                        self.access_cost += 1
                elif path[i] == '0':  # right step
                    if parent.right.check_for_item(id):
                        if self.debug:
                            print("Found item on depth " + str(i+1))    # depth + 1 because first step brings to dp=1
                        self.access_cost += 1
                        return True
                    else:
                        parent = parent.right
                        self.access_cost += 1
            return False