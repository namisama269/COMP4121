# Implementation of the Viterbi algorithm
# Examples are provided in examples folder, e.g. how to derive 
# transmission/emission matrix values
import numpy as np
from fractions import Fraction
PRECISION = 5

def viterbi(O, S, P, y, Tm, Em):
    """
    Implementation of the Viterbi algorithm.

    Input:
        O: observation space of N observations [o_0,o_1,...,o_N-1].

        S: state space of K states [s_0,s_1,...,s_K-1].

        P: initial probabilities [p_0,p_1,...,p_K-1] for each of the K states,
           where p_i is the probability that the chain starts in state s_i.

        y: list of T initial observations [y_0,y_1,...,y_T-1], each entry
           is the index of the observation in O, e.g. y_0 = 1 denotes that
           the first observation is o_1 = O[1].

        Tm: transition matrix of size K x K such that Tm[i][j] stores the
            probability that if at an instant t, the chain is at state s_i, 
            then at instant t+1, the chain is at state s_j.

        Em: emission matrix of size K x N such that Em[i][k] stores the 
            probability that if the chain is at state s_i, the observable
            outcome will be o_k.
            NOTE: first index = state, second index = emission

    Output:
        x: list of T indices [x_0,x_1,...x_T-1] of most likely states that
           generate the observations in y, access the states themselves 
           from the state space S, e.g. first state is s_(x_0) = S[x[0]]

    Implementation values:
        dp1: K x T table, dp1[i][j] stores the largest possible probability
             for which there exists a sequence [x_0,...,x_j-1] ending with 
             x_j-1 = s_i that generates the observations y = [y_0,y_1,...,y_j-1]

        dp2: K x T table, dp2[i][j] stores the index k ranging from 0 to K-1
             such that dp1[k][j-1] * Tm[k][i] * Em[i][y[j]] is maximised, this
             is equivalently the index of the candidate that was chosen for
             dp1[i][j], and is used for backtracking to find the path x of most
             likely states.

        i: index to iterate over K states
        j: index to iterate over T observations
        k: index to iterate over K states when finding maximum probability for
           subproblem dp1[i][j]

        opt: keeps track of index of the optimal path when backtracking to
           compute x

    Recurrence relation:

        Base case (dp1[i][0], j = 0): 
        = largest possible prob that there exists a sequence [s_i] that generates 
          the observations [y_0]
        = initial probability that the chain starts in s_i AND the outcome y_0
          is observed from s_i
        = P[i] * Em[i][y[0]]

        Recurrence case (dp1[i][j]):
        = largest possible prob that there exists a sequence of length j ending in s_i 
          that generates the first j observations
        A sequence of length j ending in s_i can be formed by taking ANY sequence of 
        length j-1 and adding s_i to it, given that previous sequence caused the 
        observations equal to first j-1 observations in y.
        This chain of length j-1 can end in any one of the K states.
        To get the best probability, would have to choose from the best probability 
        for the first j-1 states first, so the candidates for dp1[i][j] are:
            best probability for sequence of length j-1 ending in state s_k AND
            the sequence transitions to state s_i at the jth state AND
            the observation y_j-1 is observed (emitted) from state s_i
            = [dp1[k][j-1] * Tm[k][i] * Em[i][y[j]] for k in range(K)]
        choose the best one.
    """
    K, T = len(S), len(y)
    check_input(O, S, P, y, Tm, Em)

    # Construct the 2 dp tables with dimensions K x T
    dp1 = np.zeros((K, T))
    dp2 = np.zeros((K, T))

    # Base case: on first observation (j = 0)
    for i in range(K):
        dp1[i][0] = P[i] * Em[i][y[0]]
        dp2[i][0] = 0

    # Recurrence case
    for j in range(1, T):
        for i in range(K):
            candidates = np.array([dp1[k][j-1] * Tm[k][i] * Em[i][y[j]] for k in range(K)])
            dp1[i][j] = np.max(candidates)
            dp2[i][j] = np.argmax(candidates) 
    
    # Backtrack along dp2 to get the path
    prob = np.max([dp1[k][T-1] for k in range(K)])
    opt = np.argmax([dp1[k][T-1] for k in range(K)])
    x = [None for _ in range(T)]
    x[T-1] = opt

    for j in range(T-1, 0, -1):
        opt = int(dp2[opt][j])
        x[j-1] = opt

    return x, prob


def check_input(O, S, P, y, Tm, Em):
    """
    Check that the input has correct dimensions and values.
    """
    N, K, T = len(O), len(S), len(y)

    if len(P) != K:
        raise ValueError("K probabilites must be provided")
    if len(y) != T:
        raise ValueError("T observations must be provided")
    if np.shape(Tm) != (K, K):
        raise ValueError("Transmission matrix must have dimensions K x K")
    if np.shape(Em) != (K, N):
        print(np.shape(Tm))
        raise ValueError("Emission matrix must have dimensions K x N")
    for prob in P:
        if prob < 0 or prob > 1:
            raise ValueError("Initial probabilities must be between 0 and 1")
    for obs in y:
        if obs < 0 or obs >= N:
            raise ValueError("Each observation in y must be from 0 to N-1")
    for i in range(K):
        for j in range(K):
            if Tm[i][j] < 0 or Tm[i][j] > 1:
                raise ValueError("Transition matrix probabilities must be between 0 and 1")
    for i in range(K):
        for j in range(N):
            if Em[i][j] < 0 or Em[i][j] > 1:
                raise ValueError("Emission matrix probabilities must be between 0 and 1")

###################################################################################################
###################################################################################################

def print_result(O, S, x, y, prob, use_frac = True):
    print("The sequence most likely to cause the observation (", end="")
    for i in range(len(y)):
        print(O[y[i]], end="")
        if i != len(y)-1:
            print(", ", end="")
    print(") is:")

    print("(", end="")
    for i in range(len(x)):
        print(S[x[i]], end="")
        if i != len(x)-1:
            print(", ", end="")
    fprob = Fraction(prob).limit_denominator() if use_frac else f"{prob:.{PRECISION}f}"
    print(f") with probability {fprob}")


def viterbi_print_exec(O, S, P, y, Tm, Em, use_frac = True):
    """
    Execute the Viterbi algorithm and print the execution trace.
    """
    if use_frac:
        np.set_printoptions(formatter={'all':lambda x: str(Fraction(x).limit_denominator())})
    else:
        np.set_printoptions(precision=PRECISION)
    # idk if need to reset it after function is done

    K, T = len(S), len(y)
    check_input(O, S, P, y, Tm, Em)
    dp1 = np.zeros((K, T))
    dp2 = np.zeros((K, T))

    print(f"Base case: j = 0")
    print()
    for i in range(K):
        dp1[i][0] = P[i] * Em[i][y[0]]
        dp2[i][0] = 0
        print(f"    dp1[{i}][0] = P[{i}] * Em[{i}][y[0]] = ",end="")
        if use_frac:
            print(f"{Fraction(P[i]).limit_denominator()} * ", end="")
            print(f"{Fraction(Em[i][y[0]]).limit_denominator()} = ", end="")
            print(f"{Fraction(P[i] * Em[i][y[0]]).limit_denominator()}")
        else:
            print(f"{P[i]:.{PRECISION}f} * ", end="")
            print(f"{Em[i][y[0]]:.{PRECISION}f} = ", end="")
            print(f"{P[i] * Em[i][y[0]]:.{PRECISION}f}")
        print("    dp2[i][0] = 0")
    print()


    for j in range(1, T):
        print(f"Current iteration: j = {j}")
        print()
        for i in range(K):
            candidates = np.array([dp1[k][j-1] * Tm[k][i] * Em[i][y[j]] for k in range(K)])
            print(f"    Candidates when i = {i}:")
            for k in range(K):
                if use_frac:
                    print(f"    {Fraction(candidates[k]).limit_denominator()}", end="")
                else:
                    print(f"    {candidates[k]:.{PRECISION}f}", end="")
                print(f" = dp1[{k}][{j-1}] * Tm[{k}][{i}] * Em[{i}][y[{j}]] = ", end="")
                if use_frac:
                    print(f"{Fraction(dp1[k][j-1]).limit_denominator()} * ", end="")
                    print(f"{Fraction(Tm[k][i]).limit_denominator()} * ",end="")
                    print(f"{Fraction(Em[i][y[j]]).limit_denominator()}")
                else:
                    print(f"{dp1[k][j-1]:.{PRECISION}f} * ", end="")
                    print(f"{Tm[k][i]:.{PRECISION}f} * ", end="")
                    print(f"{Em[i][y[j]]:.{PRECISION}f}")

            print()
            if use_frac:
                print(f"    The maximum is {Fraction(np.max(candidates)).limit_denominator()}", end="")
            else:
                print(f"    The maximum is {np.max(candidates):.{PRECISION}f}", end="")
            print(f" when k = {int(np.argmax(candidates))}")
            print()
            dp1[i][j] = np.max(candidates)
            dp2[i][j] = np.argmax(candidates)

    print(f"Final dp1 table: ")
    print(dp1)
    print()
    print(f"Final dp2 table: ")
    print(dp2)
    print()

    opt = np.argmax([dp1[k][T-1] for k in range(K)])
    row = opt
    x = [None for _ in range(T)]
    x[T-1] = opt
    prob = np.max([dp1[k][T-1] for k in range(K)])
    fprob = Fraction(prob).limit_denominator() if use_frac else f"{prob:.{PRECISION}f}"

    print(f"The highest probability state has probability {fprob} and ends on state {int(opt)}")
    print()
    for j in range(T-1, 0, -1):
        opt = int(dp2[opt][j])
        x[j-1] = opt
    
    print(f"Backtracking from row {int(row)} from the right,")
    print(f"x = ", end="")
    print(x)
    print()

    return x, prob

###################################################################################################
###################################################################################################

if __name__ == "__main__":
    pass


    
