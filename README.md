# sampling [![Build Status](https://travis-ci.com/tommyod/sampling.svg?branch=master)](https://travis-ci.com/tommyod/sampling) [![PyPI version](https://badge.fury.io/py/sampling.svg)](https://pypi.org/project/sampling/) [![Documentation Status](https://readthedocs.org/projects/sampling/badge/?version=latest)](https://sampling.readthedocs.io/en/latest/?badge=latest) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Sampling algorithms implemented in pure Python 3.6+.

- Unlike the standard library `random` module, weighted sampling without replacement is implemented here.
- The `Urn` class provides a general interface for sampling which is more efficient than calling `sample` many times.

## Installation

The software is available through GitHub, and through [PyPI](https://pypi.org/project/sampling/).
You may install the software using `pip`.

```bash
pip install sampling
```

## Examples

### Basic sampling

```python
from sampling import sample

population = ['a', 'b', 'b', 'c']
weights = [7, 1, 2, 4]

# No replacement, no weights
samples = sample(population, size=2)

# With replacement and with weights
samples = sample(population, size=2, replace=True, weights=weights)
```

### Basic usage of the urn object

```python
from sampling import Urn
import itertools

population = ['a', 'b', 'b', 'c', 'd', 'e']
weights = [7, 1, 2, 4, 3, 1]

# Create an urn and draw a single sample
urn = Urn(population, weights=weights)
sample = next(urn)

# Draw 2 more samples
samples = list(itertools.islice(urn, 2))

# Draw the remaining samples
remaining_samples = list(urn)
```

### Advanced usage of the urn object

```python
from sampling import Urn

population = ['a', 'b', 'b', 'c', 'd', 'e']
weights = [7, 1, 2, 4, 3, 1]

# Create an urn and draw a single sample
urn = Urn(population, replace=True, weights=weights)

# Enter an infinite loop of sampling with replacement
for element in urn:
    # Perform logic here
    if element == "a":
        break
```


## Speed and comparison

- For many common use cases, the NumPy `np.random.choice` function is faster than this pure Python implementation.


## Contributing

You are very welcome to scrutinize the code and make pull requests if you have suggestions and improvements.
Your submitted code must be PEP8 compliant, and all tests must pass.

### Contributors

- [aredelmeier](https://github.com/aredelmeier)
- [JensWahl](https://github.com/JensWahl)
- [mojohn89](https://github.com/mojohn89)
- [tommyod](https://github.com/tommyod)
