import sys
sys.path.append('.')
import numpy as np
from hmms_viterbi.viterbi import viterbi_print_exec, print_result

"""
Raccoons and possums problem from the lecture slides.
http://www.cse.unsw.edu.au/~cs4121/lectures_2019/racoons_and_possums.pdf

In California there are twice as many raccoons as possums. Having gotten a 
job with Google, you are in California observing your back yard. It is dusk, 
so the probability that you think you saw a raccoon when you are actually 
looking at a possum at a distance is 1/3; the probability that you think you 
saw a possum while you are actually looking at a raccoon at a distance is 1/4. 
Raccoons move in packs; so if a raccoon comes to your back yard the probability 
that the next animal to follow will also be a raccoon is 4/5. Possums are 
solitary animals, so if a possum comes to your back yard, this does not impact 
the probabilities what the next animal to come will be (a possum or a raccoon,
but recall in California there are twice as many raccoons as possums!) You 
believe that you saw four animals coming in the following order: a raccoon, 
a possum, a possum, a raccoon (rppr). Given such a sequence of observations, 
what actual sequence of animals is most likely to cause such a sequence of 
your observations?
"""

"""
Solution (finding the parameters): 

To distinguish between states and observations, let the state space be R and P, 
and the observation space be r and p.

Initially, there are twice as many raccoons as possums, so the chance to see a
raccoon is 2 times the chance to see a possum at the start. Solve the equations
to get p_0 = π(R) = 2/3 and p_1 = π(P) = 1/3.

The transition probabilities are independent of any observations, so the 
information to get it does not have anything to do with "what you saw" or 
"what you think you saw". 

It is given that if a raccoon comes to your back yard the probability that 
the next animal to follow will also be a raccoon is 4/5, so P(R->R) = 
Tm[0][0] = 4/5, and by total probability, if it's not a raccoon then it has
to be a possum, so P(R->P) = Tm[0][1] = 1/5.

Since if a possum comes, it does not change the probabilities, we can just use
the initial probabilities:
P(P->P) = Tm[1][1] = π(P) = 1/3, P(P->R) = Tm[1][0] = π(R) = 2/3.

For the emission probabilities, given that you are actually looking at a possum,
the probability that you think you saw a raccoon is 1/3. 
So P(r|P) = Em[1][0] = 1/3, and by total probability, if you did not think
you saw a raccoon, then you must have thought you saw a possum, so 
P(p|P) = Em[1][1] = 2/3.

Similarly, P(p|R) = Em[0][1] = 1/4 and P(r|R) = Em[0][0] = 3/4.

NOTE: make sure the emissions index the state (R or P) first, then the 
observations (r or p).
"""

O =  ["r", "p"]
S = ["R", "P"]
P = np.array([2/3, 1/3])
y = np.array([0, 1, 1, 0])
Tm = np.array([[4/5, 1/5], [2/3, 1/3]])
Em = np.array([[3/4, 1/4], [1/3, 2/3]])

x, prob = viterbi_print_exec(O, S, P, y, Tm, Em, use_frac=True)
print_result(O, S, x, y, prob, use_frac=True)

"""
Base case: j = 0

    dp1[0][0] = P[0] * Em[y[0]][0] = 2/3 * 3/4 = 1/2
    dp2[i][0] = 0
    dp1[1][0] = P[1] * Em[y[0]][1] = 1/3 * 1/3 = 1/9
    dp2[i][0] = 0

Current iteration: j = 1

    Candidates when i = 0:
    1/10 = dp1[0][0] * Tm[0][0] * Em[y[1]][0] = 1/2 * 4/5 * 1/4
    1/54 = dp1[1][0] * Tm[1][0] * Em[y[1]][0] = 1/9 * 2/3 * 1/4

    The maximum is 1/10 when k = 0

    Candidates when i = 1:
    1/15 = dp1[0][0] * Tm[0][1] * Em[y[1]][1] = 1/2 * 1/5 * 2/3
    2/81 = dp1[1][0] * Tm[1][1] * Em[y[1]][1] = 1/9 * 1/3 * 2/3

    The maximum is 1/15 when k = 0

Current iteration: j = 2

    Candidates when i = 0:
    1/50 = dp1[0][1] * Tm[0][0] * Em[y[2]][0] = 1/10 * 4/5 * 1/4
    1/90 = dp1[1][1] * Tm[1][0] * Em[y[2]][0] = 1/15 * 2/3 * 1/4

    The maximum is 1/50 when k = 0

    Candidates when i = 1:
    1/75 = dp1[0][1] * Tm[0][1] * Em[y[2]][1] = 1/10 * 1/5 * 2/3
    2/135 = dp1[1][1] * Tm[1][1] * Em[y[2]][1] = 1/15 * 1/3 * 2/3

    The maximum is 2/135 when k = 1

Current iteration: j = 3

    Candidates when i = 0:
    3/250 = dp1[0][2] * Tm[0][0] * Em[y[3]][0] = 1/50 * 4/5 * 3/4
    1/135 = dp1[1][2] * Tm[1][0] * Em[y[3]][0] = 2/135 * 2/3 * 3/4

    The maximum is 3/250 when k = 0

    Candidates when i = 1:
    1/750 = dp1[0][2] * Tm[0][1] * Em[y[3]][1] = 1/50 * 1/5 * 1/3
    2/1215 = dp1[1][2] * Tm[1][1] * Em[y[3]][1] = 2/135 * 1/3 * 1/3

    The maximum is 2/1215 when k = 1

Final dp1 table: 
[[1/2 1/10 1/50 3/250]
 [1/9 1/15 2/135 2/1215]]

Final dp2 table: 
[[0 0 0 0]
 [0 0 1 1]]

The highest probability state has probability 3/250 and ends on state 0

Backtracking from row 0 from the right,
x = [0, 0, 0, 0]

The sequence most likely to cause the observation (r, p, p, r) is:
(R, R, R, R) with probability 3/250
"""