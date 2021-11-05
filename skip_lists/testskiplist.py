"""
Driver code to test implementation
"""
from skiplist import SkipList
import sys

def processCommands(sl, command, params):
    if command == "len":
        l = len(sl)
        print(f"There " + ("is" if l == 1 else "are") + f" {l} element" + ("s" if l != 1 else "") + " in the list")
        print()
    elif command == "in":
        if len(params) != 1:
            print("No value entered")
            print()
            return
        isIn = params[0] in sl
        print(f"{params[0]} is" + ("" if isIn else " not") + " in the list")
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
    elif command == "del" or "rem":
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
        sl.display(printDists=False)
        print()
    elif command == "q":
        sys.exit()
    elif command == "kth" or command == "ith" or command == "get":
        if len(params) < 1:
            print("No value entered")
            print()
            return
        for param in params:
            try:
                kth = sl[param]
                print(f"sl[{param}] = {kth}")
                print()
            except ValueError:
                print("Invalid k, enter k from 0 to list length-1")
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

# 3 9 17 21 25 26 27 29 34 