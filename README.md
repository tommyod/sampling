# sampling [![Build Status](https://travis-ci.com/tommyod/sampling.svg?branch=master)](https://travis-ci.com/tommyod/sampling) [![PyPI version](https://badge.fury.io/py/sampling.svg)](https://pypi.org/project/sampling/) [![Documentation Status](https://readthedocs.org/projects/sampling/badge/?version=latest)](https://sampling.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://pepy.tech/badge/sampling)](https://pepy.tech/project/sampling) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

An efficient pure Python implementation of sampling with and without replacement, with and without weights. Works with Python 3.6+.

There are four ways to sample from a list of objects:
* Sampling without replacement samples an object at random, notes the object, and then doesn't put the object back. Then samples another object. It is possible to sample as many objects as in the original list but not more. 
* Sampling with replacement samples an object at random, notes the object, and then puts the object back. Then samples another. It is possible to sample an infinite number of objects since the object is always put back after it is sampled. * Sampling without replacement, with weights. Same as above but adds weights to the desired objects. 
* Sampling with replacement with weights. Same as above but adds weights to the desired objects. 

For more information on the algorithms behind these sampling methods, see below. 

## Implementation
We use an Urn object to represent the list of objects we want to sample from. 

## Example

```python
from sampling import Urn
import random

random.seed(a = 2)

data = list('abc')

# 1.
urn = Urn(population=data, replace=False, weights=None)

x = tuple(urn)
print(x) # ('c', 'b', 'a')

# 2. sampling with replacement, no weights

urn = Urn(data, replace=True, weights=None)

y = tuple(itertools.islice(urn, len(data)))   
y2 = tuple(itertools.chain.from_iterable(y))
print(y2) # ('a', 'c', 'c')

# 3. sampling with replacement, with weights
weights = (1, 2, 3)

urn = Urn(data, replace=True, weights=weights)

z = tuple(itertools.islice(urn, len(data)))
z2 = tuple(itertools.chain.from_iterable(z))
print(z2) # ('c', 'b', 'c')

# 4. sampling without replacement, with weights
weights = (1, 2, 3)


```
More examples are included below.

## Installation

The software is available through GitHub, and through [PyPI](https://pypi.org/project/sampling/).
You may install the software using `pip`.

```bash
pip install sampling
```

## Contributing

You are very welcome to scrutinize the code and make pull requests if you have suggestions and improvements.
Your submitted code must be PEP8 compliant, and all tests must pass.
Contributors: [CRJFisher](https://github.com/CRJFisher)


## Sampling algorithms 

1. Sampling without replacement and without weights. This is done using the [Fisher-Yates shuffle] (https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle). The original method starts by writing out the list of objects (and their numerical equivalences) and chosing a number between 1 and the number of objects at random. After this number is chosen, the given object is crossed out. A new number is chosen, this time between 1 and the number of objects minus 1 (since one has just been crossed out). The new object is crossed out. This is continued until all objects are exhausted. 

This method was adapted to be faster. First, a number is again chosen between 1 and the number of objects. This time, the chosen number and the last number are switched. A second number is chosen between 1 and the number of objects minus 1. Again, the chosen number is put at the end and the last number (that still hasn't been chosen) is switched. This is continued until all objects are exhausted. 

2. Sampling with replacement and without weights. 

3. Sampling with replacement and with weights.

4. Sampling without replacement and with weights. 
