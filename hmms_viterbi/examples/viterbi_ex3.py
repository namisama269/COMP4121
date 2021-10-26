import sys
sys.path.append('.')
import numpy as np
from hmms_viterbi.viterbi import viterbi_print_exec, print_result

"""
Example from:
https://en.wikipedia.org/wiki/Hidden_Markov_model#Weather_guessing_game

Consider two friends, Alice and Bob, who live far apart from each other and 
who talk together daily over the telephone about what they did that day. 
Bob is only interested in three activities: walking in the park, shopping, 
and cleaning his apartment. The choice of what to do is determined exclusively 
by the weather on a given day. Alice has no definite information about the 
weather, but she knows general trends. Based on what Bob tells her he did 
each day, Alice tries to guess what the weather must have been like.

Alice believes that the weather operates as a discrete Markov chain. There 
are two states, "Rainy" and "Sunny", but she cannot observe them directly, 
that is, they are hidden from her. On each day, there is a certain chance 
that Bob will perform one of the following activities, depending on the 
weather: "walk", "shop", or "clean". Since Bob tells Alice about his 
activities, those are the observations. The entire system is that of a hidden 
Markov model (HMM).

Alice knows the general weather trends in the area, and what Bob likes to 
do on average. In other words, the parameters of the HMM are known. 
They can be represented as follows in Python:

    states = ('Rainy', 'Sunny')
    observations = ('walk', 'shop', 'clean')
    start_probability = {'Rainy': 0.6, 'Sunny': 0.4}
    transition_probability = {
        'Rainy' : {'Rainy': 0.7, 'Sunny': 0.3},
        'Sunny' : {'Rainy': 0.4, 'Sunny': 0.6},
    }
    emission_probability = {
        'Rainy' : {'walk': 0.1, 'shop': 0.4, 'clean': 0.5},
        'Sunny' : {'walk': 0.6, 'shop': 0.3, 'clean': 0.1},
    }

In this piece of code, start_probability represents Alice's belief about which 
state the HMM is in when Bob first calls her (all she knows is that it tends 
to be rainy on average). The particular probability distribution used here is 
not the equilibrium one, which is (given the transition probabilities) 
approximately {'Rainy': 0.57, 'Sunny': 0.43}. The transition_probability 
represents the change of the weather in the underlying Markov chain. In this 
example, there is only a 30% chance that tomorrow will be sunny if today is 
rainy. The emission_probability represents how likely Bob is to perform a 
certain activity on each day. If it is rainy, there is a 50% chance that he is 
cleaning his apartment; if it is sunny, there is a 60% chance that he is 
outside for a walk.
"""

# Problem: what are the most likely states on 5 days that Bob did the following:
# clean, shop, walk, walk, shop? 

O = ["walk", "shop", "clean"]
S = ["rainy", "sunny"]
P = np.array([0.6, 0.4])
y = np.array([2, 1, 0, 0, 1])
Tm = np.array([[0.7, 0.3], [0.4, 0.6]])
Em = np.array([[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]])

x, prob = viterbi_print_exec(O, S, P, y, Tm, Em, use_frac=False)
print_result(O, S, x, y, prob, use_frac=False)

"""
The sequence most likely to cause the observation (clean, shop, walk, walk, shop) 
is:
(rainy, rainy, sunny, sunny, sunny) with probability 0.00098
"""