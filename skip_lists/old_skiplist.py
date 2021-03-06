"""
Based on:
https://github.com/kunigami/blog-examples/blob/master/skip-list/skipList.py
https://www.geeksforgeeks.org/skip-list-set-2-insertion/
"""

import random
import sys

class SkipNode:
    """
    A node in the skip list. Stores a value and pointers to next nodes on all levels.
    """
    def __init__(self, level=0, val=None):
        self.val = val
        self.next = [None] * (level+1)

    def getTopLevel(self):
        return len(self.next) - 1

class SkipList:
    """
    Skip list class. Levels are indexed from 0.
    Atributes:
    - head node: has next pointers to all levels
    - len: number of elements in the skip list
    - top: number of levels in the node with the most number of levels
    - maxLevel: upper bound on number of levels, fixed at initialisation
    Public methods: 
    - __len__: get the number of elements in the skip list
    - contains: check if the list contains a certain value
    - isEmpty: check if the list is empty
    - insert: insert a value into the skip list
    - remove: remove a value from the skip list
    - __str__: display elements of the skip list in list form
    - displayList: display level structure of the skip list
    """

    def __init__(self, maxLevel):
        self.head = SkipNode(maxLevel)
        self.len = 0
        self.top = 0
        self.maxLevel = maxLevel

    def __len__(self):
        """
        Get the number of elements in the skip list.
        """
        return self.len

    def search(self, val, update=None):
        """
        Search for given value, return pointer to its node if found, None if not found.
        """
        # Get the update list if not passed in (from other uses)
        if update is None:
            update = self.getUpdateList(val)

        # Check the lowest level since all elements are linked there
        # If the previous value's next is the required value itself, then 
        # it has been found
        candidate = update[0].next[0] if update[0] is not None else None
        if candidate is not None and candidate.val == val:
            return candidate
        return None

    def contains(self, val, update=None):
        """
        Check if the list contains a certain value.
        """
        return self.search(val, update) is not None

    def randomLevel(self):
        """
        Get a random level by tossing a coin until getting a head (0) and counting how many tails (1) were landed.
        Stop early if the maximum allowed level is reached.
        """
        level = 0
        while random.randint(0, 1) == 1 and level < self.maxLevel:
            level += 1
        return level

    def getUpdateList(self, val):
        """
        Get the list of nodes preceding the node with given value at every level.
        If the value is in the list, return the nodes that would precede the value
        if it was in the list.
        """
        update = [None] * (self.top+1)
        curr = self.head

        # Loop from top floor to bottom floor
        for i in range(self.top, -1, -1):
            # Move to next value if before the end and still smaller than search value
            while curr.next[i] is not None and curr.next[i].val < val:
                curr = curr.next[i]
            update[i] = curr
        return update

    def insert(self, val):
        """
        Insert a value into the skip list. Return the value if successfully inserted,
        None if not.
        """
        # Create new node for the value with a random level
        newNode = SkipNode(self.randomLevel(), val)

        # Update the list's top level if this random level is higher than any
        # existing level
        self.top = max(self.top, newNode.getTopLevel())

        # Get the update list for the value to be inserted
        update = self.getUpdateList(val)

        # Insert the value if it is not already in the list
        if self.search(val, update) is None:
            # Link all next pointers on each level 
            for i in range(newNode.getTopLevel()+1):
                # New node's nexts are the previous node's nexts, and the previous node's
                # nexts are the new node
                newNode.next[i] = update[i].next[i]
                update[i].next[i] = newNode

            # Update the length of the list after a successful insertion
            self.len += 1

            return val

        return None

    def remove(self, val):
        """
        Remove a value from the skip list. Return the value if successfully removed,
        None if not.
        """
        # Get the update list for the value to be inserted
        update = self.getUpdateList(val)

        # Remove the value if it is found in the list
        curr = self.search(val, update)
        if curr is not None:
            # Fix links on each level
            for i in range(curr.getTopLevel(), -1, -1):
                # The previous node's nexts are now the node to delete's nexts.
                update[i].next[i] = curr.next[i]

                # If deletion forced the node with highest level to be gone, the head's
                # next pointer at that level would no longer point to any node, so
                # the max height is decreased
                if self.head.next[i] is None:
                    self.top -= 1

            # Update the length of the list after a successful deletion
            self.len -= 1
            return val

        return None

    def __str__(self):
        """
        Display elements of the skip list in list form.
        """

        # All elements are on level 0 so use that to get all values
        outStr = "["
        i = 0
        node = self.head.next[0]
        while node is not None:
            outStr += str(node.val)
            if i != self.len - 1:
                outStr += ", "
            i += 1
            node = node.next[0]

        return outStr + "]"

    def displayList(self):
        """
        Display level structure of the skip list.
        """
        print("\n*****Skip List******")
        head = self.head
        for lvl in range(self.top+1):
            print("Level {}: ".format(lvl), end=" ")
            node = head.next[lvl]
            while(node != None):
                print(node.val, end=" ")
                node = node.next[lvl]
            print("")


def processCommands(sl, command, params):
    if command == "len":
        l = len(sl)
        print(f"There " + "is" if l == 1 else "are" + f" {l} element" + "s" if l != 1 else "" + "in the list")
        print()
    elif command == "in":
        if len(params) != 1:
            print("No value entered")
            print()
            return
        isIn = sl.contains(params[0])
        print(f"{params[0]} is" + "" if isIn else "not" + " in the list")
        print()
    elif command == "ins":
        if len(params) < 1:
            print("No value entered")
            print()
            return
        for param in params:
            ins = sl.insert(param)
            if ins:
                print(f"Successfully inserted {param} into the list")
            else:
                print(f"{param} is already in the list, cannot insert")
        print()
    elif command == "del":
        if len(params) < 1:
            print("No value entered")
            print()
            return
        for param in params:
            dl = sl.remove(param)
            if dl:
                print(f"Successfully deleted {param} from the list")
            else:
                print(f"{param} is not in the list, cannot delete")
        print()
    elif command == "str":
        print(str(sl))
        print()
    elif command == "show":
        sl.displayList()
        print()
    else:
        print("Invalid command, try again")
        print()



if __name__ == "__main__":
    # Enter argument for max level of skip list in command line
    maxLevel = int(sys.argv[1])
    sl = SkipList(maxLevel)
    print(f"Initialised skip list with maximum {maxLevel+1} levels")
    print("Enter commands from {len, in, ins, del, str, show}")
    print()

    while True:
        try:
            inp = input().split()
            if len(inp) < 1:
                continue
            command = inp[0]
            params = [] if len(inp) == 1 else [int(x) for x in inp[1:]]
            processCommands(sl, command, params)
        except EOFError:
            break