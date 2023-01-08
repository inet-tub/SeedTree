from pushdown.treeStructure import *
import random
import time

class randomPush():

    def __init__(self, tree, single_capacity = False):
        """ Definition of the random-push algorithm-params
            @param single_capacity: set to True if servers have capacity=1
            """
        self.debug = False
        self.tree = tree
        self.max_pushed_level = 0
        self.last_reached_server = None     # used in make_avail and pushdown_path
        self.single_capacity = single_capacity

        # counters for evaluation
        self.n_accesses = 0
        self.access_cost = 0
        self.moves = 0      # moving cost
        self.reconfig = 0   # searching-for-a-path cost

    """
    def reset(self):
        self.moves = 0
        self.adjust_cost = 0
        self.access_cost = 0"""

    def access(self, item_id):
        self.n_accesses += 1
        if self.debug:
            print("\nRandom Push-Access " + str(item_id))

        if not self.pull_up_item(item_id):
            raise Exception("No Item for " + str(item_id) + " found")
        else:
            if self.debug:
                print_tree(self.tree.root)

    def pull_up_item(self, item_id):
        """ pulls up v,
            pushes root down one step along the path to random_item at v.dep """
        parent = self.tree.root
        #if type(item_id) == int:
        path = self.tree.get_hash(item_id)
     #   else:
      #      path = self.tree.get_hash_str(item_id)
        if self.debug:
            print("Got hash " + str(path) + " for item " + str(item_id))
        if parent.check_for_item(item_id):      # root access
            return True
        else:       # item not found at root
            for i in range(0, len(path)):
                if not path[i]:
                    raise Exception("No step left in path!")
                elif path[i] == '1':      # left step
                    if parent.left.remove_item(item_id):
                        if self.debug:
                            print("Found item on depth " + str(i+1))    # depth + 1 because first step brings to dp=1
                            self.moves += i+1           # add cost for pull up the item to root
                        return self.init_procedure(item_id=item_id, depth=i+1)
                    else:
                        parent = parent.left
                        self.access_cost += 1         # add cost for iterating down a level
                else:           # right step
                    if parent.right.remove_item(item_id):
                        if self.debug:
                            print("Found item on depth " + str(i+1))
                            self.moves += i + 1
                        return self.init_procedure(item_id=item_id, depth=i+1)
                    else:
                        parent = parent.right
                        self.access_cost += 1       # add cost for iterating down a level
            return False

    def init_procedure(self, item_id, depth):
        """
        Move the item up to the root and start the algo:
        first check for a free path and save it
        Second, start pushing down the items along the path
        """
        if self.single_capacity:
            self.tree.root.insert(item_id, buffer=True)
        else:
            self.tree.root.insert(item_id)
        trials = int(self.tree.initial_occupation) * 100
        #for j in range(0, trials):
        start = time.time()
        elapsed = 0
        while elapsed < 30:  # while less than 30 seconds have elapsed
            path_trial = self.check_path(depth=depth)
            #if j > trials*0.9:     # print log if we get to difficulties
            if elapsed > 28:
                self.debug = True
            if path_trial:
                self.pushdown_path(found_path=path_trial)
                return True
            elapsed = time.time() - start  # update the time elapsed
        if self.debug:
            print("No path found for tree:")
        print_tree(self.tree.root)
        raise Exception("No path found after " + str(trials) + " trials")

    def check_path(self, depth):
        """ check for a free path to v.dep
        @:param id = id of the item to place on the root
        @:param depth = depth of the pulled up item - the random path will be of this depth
        returns the found path, or None if failed """
        parent = self.tree.root
        random_candidates = parent.slots.copy()  # for the root level, save candidates before adding new one
        i = 0
        found_path = []
        if depth == 0:
            random_item = random.choice(tuple(random_candidates))
            for i in range(0, 10):  # 10 tentatives to find free item on level 1
                found_path = self.check_onelevel(random_item)
                self.reconfig += 1
                if found_path: return found_path
            raise Exception("No path found for push to first level")

        # depth > 0
        while i < depth:
            if i > 0:
                random_candidates = parent.slots.copy()        # take all the items as candidates for the other levels
            if not random_candidates:       # if the slot is empty, it will only be temporarily
                random_item = found_path[len(found_path)-1]     # take the last item, which will be moved down from upper level
            else:
                if found_path:
                    random_candidates.add(found_path[len(found_path)-1])     # add last item (moved down from level above) to choice
                random_item = random.choice(tuple(random_candidates))
                if self.debug:
                    print("Chose " + str(random_item) + " randomly from " + str(random_candidates) + ", dep = "
                          + str(len(found_path)))
            if self.tree.get_hash(random_item)[i] == '1':
                if i == (depth-1) and not self.verify_spot(parent.left):       # if there is no slot left
                    if self.debug:
                        print("Reached item " + str(random_item) + " at level " + str(i) +
                              ", trying LEFT step, bitstr(item): " + self.tree.get_hash(random_item) +
                              ", trying to insert in " + str(parent.left.slots) + "; no path found")
                    self.reconfig += i       # add cost to move back to root
                    return None        # restart the procedure
                found_path.append(random_item)
                parent = parent.left
            elif self.tree.get_hash(random_item)[i] == '0':
                if i == (depth-1) and not self.verify_spot(parent.right):
                    if self.debug:
                        print("Reached item " + str(random_item) + " at level " + str(i) +
                              ", trying RIGHT step, bitstr(item): " + self.tree.get_hash(random_item) +
                              ", trying to insert in " + str(parent.right.slots) + "; no path found")
                    self.reconfig += i   # add cost to move back to root
                    return None  # restart the procedure
                found_path.append(random_item)
                parent = parent.right
            i += 1
            self.reconfig += 1  # add cost for accessing item along the (tentative) path
        if self.debug:
            print("Final server: " + str(parent.slots))
        self.reconfig += i   # add cost to move back to root
        return found_path

    def pushdown_path(self, found_path):
        """ pushes down items along random path (pre-determined by check_path)
        @:param found_path = previously, randomly found free path  """
        parent = self.tree.root
        i = 0
        while i<len(found_path):
            moving_item = found_path[i]
            if parent.remove_item(moving_item):
                if self.debug:
                    print("(!!) Pushing down item " + str(moving_item) + " to dep " + str(i+1) + " with step: " +
                          str(self.tree.get_hash(moving_item)[i]) + ", hash = " + str(self.tree.get_hash(moving_item)))
            #self.max_pushed_level = i + 1
            #bef_making_space = self.moves  # used to record current depth before eventually starting make_avail
            if self.tree.get_hash(moving_item)[i] == '1':
                parent.left.insert(moving_item, buffer = True)
                parent = parent.left
            elif self.tree.get_hash(moving_item)[i] == '0':
                parent.right.insert(moving_item, buffer = True)
                parent = parent.right
            #movements = self.moves - bef_making_space
            #i += movements  # count how many items were pushed additionally
            #if movements > 0:
             #   parent = self.last_reached_server       # jump to the last server used by make_avail
            i += 1
            self.moves += 1  # add cost for moving item from parent to child

    def check_onelevel(self, random_item):
        if self.tree.get_hash(random_item)[0] == '1':
            if not self.verify_spot(self.tree.root.left):
                return None
            else:
                return [random_item]
        else:
            if not self.verify_spot(self.tree.root.right):
                return None
            else:
                return [random_item]

    def verify_spot(self, server):
        return server.get_current_occupation() < server.capacity