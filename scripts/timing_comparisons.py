import numpy as np
import matplotlib.pyplot as plt
import time
from sampling import Urn
import itertools
import statistics
import random

num_runs = 10

# Case 1 - No weights without replacement
def time_numpy(N, k, replace, weights):
    population = np.random.random(N)
    weights = np.random.random(N) if weights else None
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        # Sampling
        if weights is not None:
            weights = np.array(weights)
            weights = weights / np.sum(weights)
        np.random.choice(population, k, replace, weights)
        times.append(time.time() - start_time)
    return statistics.median(times)


# Case 1 - No weights without replacement
def time_numpy_with_conversion(N, k, replace, weights):
    population = [random.random() for _ in range(N)]
    weights = [random.random() for _ in range(N)] if weights else None
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        # Sampling
        if weights is not None:
            weights = np.array(weights)
            weights = weights / np.sum(weights)
        list(np.random.choice(population, k, replace, weights))
        times.append(time.time() - start_time)
    return statistics.median(times)


def time_sampling_package(N, k, replace, weights):
    population = [random.random() for _ in range(N)]
    weights = [random.random() for _ in range(N)] if weights else None
    times = []
    for _ in range(num_runs):
        start_time = time.time()
        # Sampling
        list(itertools.islice(Urn(population, replace, weights), k))
        times.append(time.time() - start_time)
    return statistics.median(times)


N = 1000
k_values = [10 ** k for k in range(4)]
"""
numpy_times = [time_numpy(N, k, False, None) for k in k_values]
plt.plot(k_values, numpy_times, label="NumPy Times")

numpy_times_conv = [time_numpy_with_conversion(N, k, False, None) for k in k_values]
plt.plot(k_values, numpy_times_conv, label="NumPy Times with conversion")

sampling_times = [time_sampling_package(N, k, False, None) for k in k_values]
plt.plot(k_values, sampling_times, label="Sampling Pkg Times with conversion")

plt.legend()
plt.ylim([0,plt.ylim()[1]])
plt.grid()
plt.show()
"""
i = 1
for replace in [True, False]:
    for weights in [True, None]:
        plt.subplot(2, 2, i)

        plt.title(label=f"Replace = {replace}, Weights = {weights}")
        numpy_times_conv = [time_numpy_with_conversion(N, k, replace, weights) for k in k_values]
        plt.plot(k_values, numpy_times_conv, label="NumPy Times with conversion")

        numpy_times_conv = [time_numpy_with_conversion(N, k, replace, weights) for k in k_values]
        plt.plot(k_values, numpy_times_conv, label="NumPy Times with conversion")

        sampling_times = [time_sampling_package(N, k, replace, weights) for k in k_values]
        plt.plot(k_values, sampling_times, label="Sampling Pkg Times with conversion")
        i += 1
        plt.legend()
        plt.ylim([0, plt.ylim()[1]])
        plt.grid()
plt.show()


# numpy_times_with_conversion
"""
for k in k_values:
    k = 10**k
    print(k, time_numpy(N, k, replace=False, weights=None), 
    time_numpy_with_conversion(N, k, replace=False, weights=None), 
    time_sampling_package(N, k, replace=False, weights=None)
    )
"""
# plt.plot()
