# sampling [![Build Status](https://travis-ci.com/tommyod/sampling.svg?branch=master)](https://travis-ci.com/tommyod/sampling) [![PyPI version](https://badge.fury.io/py/sampling.svg)](https://pypi.org/project/sampling/) [![Documentation Status](https://readthedocs.org/projects/sampling/badge/?version=latest)](https://sampling.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://pepy.tech/badge/sampling)](https://pepy.tech/project/sampling) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

An efficient pure Python implementation of sampling with and without replacement, with and without weights. Works with Python 3.6+.

## Getting started
We use an Urn object to represent the collection of objects we want to sample from. See examples below.

### Example 1 - Four sampling techniques with wrapper
```python
from sampling import sample
data = ['a','b','b','c']
weights = [1., 1.1, 1.5, 2.]
samples_count = 3

# No replacement, no weights
sample1 = sample(data, samples_count)
# With replacement, no weights
sample2 = sample(data, samples_count, replace=True)
# No replacement, with weights
sample3 = sample(data, samples_count, weights=weights)
# With replacement, with weights
replace_weights = sample(data, samples_count, replace=True, weights=weights)
```

### Example 2 - Four sampling techniques with the Urn object
```python
from sampling import Urn
data = [1,2,3,4]

# 1. sampling without replacement, no weights
urn = Urn(population=data, replace=False, weights=None)
example1 = tuple(urn)
print(example1)

# 2. sampling with replacement, no weights
urn = Urn(data, replace=True, weights=None)
example2 = tuple(itertools.islice(urn, len(data)))   
print(example2)

# 3. sampling with replacement, with weights
urn = Urn(data, replace=True, weights=(1, 1, 2, 2))
example3 = tuple(itertools.islice(urn, len(data)))
print(example3)

# 4. sampling without replacement, with weights
urn = Urn(data, replace=False, weights=(1, 1, 2, 2))
example4 = tuple(itertools.islice(urn, len(data)))
print(example4)
```

## Installation

The software is available through GitHub, and through [PyPI](https://pypi.org/project/sampling/).
You may install the software using `pip`.

```bash
pip install sampling
```

## Contributing

You are very welcome to scrutinize the code and make pull requests if you have suggestions and improvements.
Your submitted code must be PEP8 compliant, and all tests must pass.
Contributors: [aredelmeier](https://github.com/aredelmeier), [mojohn89](https://github.com/mojohn89), [JensWahl](https://github.com/JensWahl)
