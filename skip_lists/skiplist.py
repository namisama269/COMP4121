"""
Implementation of slip list with added functionality to search for kth element
"""
import random

class SkipNode:
    """
    A node in the skip list. Stores a value and pointers to next nodes on all levels.

    Extra: store an array of distances on each level, which is equal to how many 
    elements between the value and its next, excluding start and including end.
    Distance on level 0 is always 1.
    """

    def __init__(self, maxLevel, level=0, val=None):
        self.val = val
        self.nexts = [None] * (maxLevel+1)
        self.dists = [1] * (maxLevel+1)
        self.level = level

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
    - empty: check if the list is empty
    - insert: insert a value into the skip list
    - remove: remove a value from the skip list
    - __str__: display elements of the skip list in list form
    - display: display level structure of the skip list
    """

    def __init__(self, maxLevel):
        self.head = SkipNode(maxLevel, maxLevel)
        self.len = 0
        self.top = 0
        self.maxLevel = maxLevel
    
    def __len__(self):
        """
        Get the number of elements in the skip list.
        """
        return self.len

    def empty(self):
        return self.len == 0

    def search(self, val, prevs=None):
        """
        Search for given value, return pointer to its node if found, None if not found.
        """
        # Get the prevs list if not passed in (from other uses)
        if prevs is None:
            prevs = self.getPrevsList(val)

        # Check the lowest level since all elements are linked there
        # If the previous value's next is the required value itself, then 
        # it has been found
        candidate = prevs[0].nexts[0] if prevs[0] is not None else None
        if candidate is not None and candidate.val == val:
            return candidate
        return None

    def __getitem__(self, k):  
        """
        Get the kth element of the list in O(log n) time using modified search
        with distances.
        """
        if k not in range(0, self.len):
            raise ValueError("k not in range(0, len)")

        # Start index from 0 to be consistent with array indexing
        k += 1

        # Go next on a level while subtracting the distance to next does not
        # exceed k, if cannot go further then go down
        # Always reaches k since at the lowest level the distance increment
        # is always 1
        curr = self.head
        for lvl in range(self.maxLevel, -1, -1):
            while k >= curr.dists[lvl]:
                k -= curr.dists[lvl]
                curr = curr.nexts[lvl]
        return curr.val

    def __contains__(self, val, prevs=None):
        """
        Check if the list contains a certain value.
        """
        return self.search(val, prevs) is not None

    def randomLevel(self):
        """
        Get a random level by tossing a coin until getting a head (0) and counting how many tails (1) were landed.

        Stop early if the maximum allowed level is reached.
        """
        level = 0
        while random.randint(0, 1) == 1 and level < self.maxLevel:
            level += 1
        return level

    def getPrevsList(self, val):
        """
        Get the list of nodes preceding the node with given value at every level.
        If the value is in the list, return the nodes that would precede the value
        if it was in the list.
        """
        prevs = [None]* (self.maxLevel+1)#[self.head] * (self.maxLevel+1)
        curr = self.head
        
        # Loop from top floor to bottom floor
        for i in range(self.maxLevel, -1, -1):
            # Move to next value if before the end and still smaller than search value
            while curr.nexts[i] is not None and curr.nexts[i].val < val:
                curr = curr.nexts[i]
            prevs[i] = curr
        return prevs

    def insert(self, val):
        """
        Insert a value into the skip list. Return the value if successfully inserted,
        None if not.
        """
        # Create new node for the value with a random level
        newNode = SkipNode(self.maxLevel, self.randomLevel(), val)

        # Update the list's top level if this random level is higher than any
        # existing level
        self.top = max(self.top, newNode.level)

        # Get the prevs list for the value to be inserted
        prevs = self.getPrevsList(val)
        
        # Insert the value if it is not already in the list
        if self.search(val, prevs) is None:
            # Link all next pointers on each level 
            for i in range(newNode.level+1):

                # New node's nexts are the previous node's nexts, and the previous node's
                # nexts are the new node
                if i < newNode.level+1:
                    newNode.nexts[i] = prevs[i].nexts[i]
                    prevs[i].nexts[i] = newNode

            # Update the distances to the next node on each level
            for i in range(self.maxLevel+1):
                # Since all nodes are connected on the bottom level, the distance to
                # the next node is always 1
                if i == 0:
                    newNode.dists[i] = 1
                else:
                    # Find the new node's previous pointer
                    prevHead = prevs[i]
                    # Search on the level below for the distance between the prev 
                    # and new node, since it is the highest level that both nodes are 
                    # guaranteed to have links on
                    prevDist = 0
                    # Add the distances from all nodes in between on the level below
                    while prevHead is not None:
                        if prevHead == prevs[i].nexts[i]: 
                            break
                        prevDist += prevHead.dists[i-1]
                        prevHead = prevHead.nexts[i-1]

                    # Now do the same from the new node to its next, iterating on
                    # the level below to get its distance
                    currDist = 0
                    prevHead = newNode
                    while prevHead is not None and prevHead != newNode.nexts[i]: # IMPORTANT TODO
                        currDist += prevHead.dists[i-1]
                        prevHead = prevHead.nexts[i-1]

                    prevs[i].dists[i] = prevDist
                    if prevs[i].nexts[i] == newNode:
                        newNode.dists[i] = currDist
                    else:
                        newNode.dists[i] = 0
                    
            # Update the length of the list after a successful insertion
            self.len += 1
            return val
        
        return None

    def remove(self, val):
        """
        Remove a value from the skip list. Return the value if successfully removed,
        None if not.
        """
        # Get the prevs list for the value to be inserted
        prevs = self.getPrevsList(val)

        # Remove the value if it is found in the list
        curr = self.search(val, prevs)
        if curr is not None:
            # Fix links on each level
            for i in range(self.maxLevel, -1, -1):
                # Update the previous node's distance by adding on the current
                # node's distance
                if i > 0:
                    prevs[i].dists[i] += (curr.dists[i]-1)

            # The previous node's nexts are now the node to delete's nexts.
            for i in range(curr.level, -1, -1):
                prevs[i].nexts[i] = curr.nexts[i]

            # If deletion forced the node with highest level to be gone, the head's
            # next pointer at that level would no longer point to any node, so
            # the max height is decreased
            while self.top >= 0 and self.head.nexts[self.top] is None:
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
        node = self.head.nexts[0]
        while node is not None:
            outStr += str(node.val)
            if i != self.len - 1:
                outStr += ", "
            i += 1
            node = node.nexts[0]

        return outStr + "]"

    def display(self, printDists=True):
        """
        Display level structure of the skip list.
        """
        print("\n******Skip List******")
        head = self.head
        for lvl in range(self.top+1):
            print("Level {}: ".format(lvl), end=" ")
            node = head.nexts[lvl]
            while(node != None):
                print(node.val, end=" ")
                node = node.nexts[lvl]
            print("")
        # Print distances (for debugging)
        if not printDists:
            return
        print()
        print("H: ", end='')
        print(head.dists)
        for lvl in range(1):
            node = head.nexts[lvl]
            while(node != None):
                print(f"{node.val}: {node.dists}")
                node = node.nexts[lvl]







