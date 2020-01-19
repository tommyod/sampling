from sampling import Urn
from collections import Counter
import matplotlib.pyplot as plt
from scipy.stats import binom
import itertools


# choose your parameters

data = list('abc')
# N_list = [100000] # number of samples
N_list = [100, 10000, 1000000]
weights = (1, 2, 3)

# 1. replacement and no weights

for N in N_list:
    master_list = [tuple(Urn(population = data, replace = False)) for i in range(N)]

    counts = Counter(master_list)
    
    x = list(counts.keys())
    y = [counts[x_i] for x_i in x]
    
    plt.bar(range(len(y)), y)
    plt.title(f"Frequency of different comb, replacement, no weights, N = {N}", fontdict = {'fontsize': 8.5}, loc='center')
    plt.show()  




p = 0.5
x = 99
prob = binom.cdf(x, N, p)


# 2. replacement and weights

for N in N_list:
    master_list = [tuple(itertools.islice(Urn(data, replace = True, weights = weights), len(data))) for i in range(N)]
    
    concat_list = list(itertools.chain.from_iterable(master_list))
    # print(concat_list)
    
    counts = Counter(concat_list)
    # print(counts)
    x = list(sorted(counts.keys()))
    y = [counts[x_i] for x_i in x]
    
    plt.bar(x, y)
    plt.title(f"Frequency of different comb, replacement, weights = {weights}, N = {N}", fontdict = {'fontsize': 8.5}, loc='center')
    plt.show() 



# 3. without replacement and no weights

for N in N_list:
    master_list = [tuple(itertools.islice(Urn(data, replace = True), len(data))) for i in range(N)]
    
    concat_list = list(itertools.chain.from_iterable(master_list))
    # print(concat_list)
    
    counts = Counter(concat_list)
    
    x = list(sorted(counts.keys()))
    y = [counts[x_i] for x_i in x]
    
    plt.bar(range(len(y)), y)
    plt.title(f"Frequency of different comb, without replacement, no weights, N = {N}", fontdict = {'fontsize': 8.5}, loc='center')
    plt.show()


# master_list = [tuple(Urn(population = x, replace = True)) for i in range(N)]

# print(master_list)



