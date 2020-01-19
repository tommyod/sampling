from sampling import Urn
from collections import Counter
import matplotlib.pyplot as plt
# from scipy.stats import binom
import itertools
import math

data = list('abc')
n = len(data)
N = 1000 # number of samples
weights = (1, 2, 3)


# 1. sample without replacement, no weights

master_list = [tuple(Urn(population=data, replace=False, weights=None)) for i in range(N)]
counts = Counter(master_list)

x = list(counts.keys())
y = [counts[x_i] for x_i in x]

separator = ''
output = [separator.join(x_i) for x_i in x]

#plt.bar(output, y)
#plt.title(f"Frequency of different comb, no replacement, no weights, N = {N}", 
#          fontdict = {'fontsize': 8.5}, loc='center')
#plt.axhline(y=(1/math.factorial(n) * N), linewidth=4, color='r')
#plt.show() 

# 2. sample with replacement, no weights
master_list = [tuple(itertools.islice(Urn(data, replace=True, weights=None), 
                                      len(data))) for i in range(N)]
counts = Counter(master_list)

x = list(counts.keys())
y = [counts[x_i] for x_i in x]

separator = ''
output = [separator.join(x_i) for x_i in x]

#plt.bar(output, y)
#plt.title(f"Frequency of different comb, replacement, no weights, N = {N}", 
#          fontdict = {'fontsize': 8.5}, loc='center')
#plt.xticks(rotation=90)
#plt.axhline(y=(1 / math.pow(n, n) * N), linewidth=4, color='r')
#plt.show() 

        


# 3. sample with replacement, with weights


# make probability of each weight

# weights = (1, 2, 3)
# a = 1
# b = 2
# c = 3

S = sum(weights)

# (1/math.pow(S, n)) * 

prob_dic = {}
for i in range(len(weights)):
    prob_dic[data[i]] = weights[i]
    

def probability(probs, V):
    sum_weights = sum(probs.values())
    final_prob = 1
    for element in V:
        final_prob *= probs[element] / sum_weights
    return final_prob

    
from itertools import combinations

comb = list(combinations(data, 3))
print(comb)

comb_dic = {}
for i in range(len(comb)):
    comb_dic[comb[i]] = probability(probs=prob_dic, V=comb[i])

print(comb_dic)




master_list = [tuple(itertools.islice(Urn(data, replace = True, weights = weights), 
                                      len(data))) for i in range(N)]
counts = Counter(master_list)

x = list(counts.keys())
y = [counts[x_i] for x_i in x]

separator = ''
output = [separator.join(x_i) for x_i in x]



#plt.bar(output, y)
#plt.title(f"Frequency of different comb, replacement, weights = {weights}, N = {N}", 
#          fontdict = {'fontsize': 8.5}, loc='center')
#plt.xticks(rotation=90)
#plt.axhline(y=(1 / math.pow(n, n) * N), linewidth=4, color='r')
#plt.show() 

# 4. sample without replacement, with weights



