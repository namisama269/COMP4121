from timeit import default_timer as timer
import random
from bubblesort import bubblesort
from quicksort import quicksort
import sys

sys.setrecursionlimit(100000)

n = 10000
randlist = [random.randint(1,n) for _ in range(n)]
revlist = [x for x in range(n,0,-1)]
sortlist = [x for x in range(1,n+1)]

start = timer()
quicksort(randlist)
end = timer()
print(f"time to quicksort random list with size {n}: ")
print(end - start)

start = timer()
quicksort(revlist)
end = timer()
print(f"time to quicksort reversed list with size {n}: ")
print(end - start)

start = timer()
quicksort(sortlist)
end = timer()
print(f"time to quicksort sorted list with size {n}: ")
print(end - start)