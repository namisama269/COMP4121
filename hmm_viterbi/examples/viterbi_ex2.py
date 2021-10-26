import sys
sys.path.append('.')
import numpy as np
from hmm_viterbi.viterbi import viterbi_print_exec, print_result

"""
Example from https://en.wikipedia.org/wiki/Viterbi_algorithm#Example.

Consider a village where all villagers are either healthy or have a fever 
and only the village doctor can determine whether each has a fever. 
The doctor diagnoses fever by asking patients how they feel. The villagers 
may only answer that they feel normal, dizzy, or cold.

The doctor believes that the health condition of his patients operates as 
a discrete Markov chain. There are two states, "Healthy" and "Fever", but 
the doctor cannot observe them directly; they are hidden from him. On each 
day, there is a certain chance that the patient will tell the doctor he is 
"normal", "cold", or "dizzy", depending on his health condition.

The observations (normal, cold, dizzy) along with a hidden state 
(healthy, fever) form a hidden Markov model (HMM), and can be represented as 
follows in the Python programming language:

    obs = ("normal", "cold", "dizzy")
    states = ("Healthy", "Fever")
    start_p = {"Healthy": 0.6, "Fever": 0.4}
    trans_p = {
        "Healthy": {"Healthy": 0.7, "Fever": 0.3},
        "Fever": {"Healthy": 0.4, "Fever": 0.6},
    }
    emit_p = {
        "Healthy": {"normal": 0.5, "cold": 0.4, "dizzy": 0.1},
        "Fever": {"normal": 0.1, "cold": 0.3, "dizzy": 0.6},
    }

In this piece of code, start_p represents the doctor's belief about which 
state the HMM is in when the patient first visits (all he knows is that 
the patient tends to be healthy). The particular probability distribution 
used here is not the equilibrium one, which is (given the transition 
probabilities) approximately {'Healthy': 0.57, 'Fever': 0.43}. The 
transition_p represents the change of the health condition in the underlying 
Markov chain. In this example, there is only a 30% chance that tomorrow the 
patient will have a fever if he is healthy today. The emit_p represents how 
likely each possible observation, normal, cold, or dizzy is given their 
underlying condition, healthy or fever. If the patient is healthy, there 
is a 50% chance that he feels normal; if he has a fever, there is a 60% 
chance that he feels dizzy.

The patient visits three days in a row and the doctor discovers that on the 
first day he feels normal, on the second day he feels cold, on the third day 
he feels dizzy. The doctor has a question: what is the most likely sequence 
of health conditions of the patient that would explain these observations?
"""

# Make sure to match the indices to the state/observation space
O = ["normal", "cold", "dizzy"]
S = ["healthy", "fever"]
P = np.array([0.6, 0.4])
y = np.array([0, 1, 2])
Tm = np.array([[0.7, 0.3], [0.4, 0.6]])
Em = np.array([[0.5, 0.4, 0.1], [0.1, 0.3, 0.6]])

x, prob = viterbi_print_exec(O, S, P, y, Tm, Em, use_frac=False)
print_result(O, S, x, y, prob, use_frac=False)

"""
The sequence most likely to cause the observation (normal, cold, dizzy) is:
(healthy, healthy, fever) with probability 0.01512
"""