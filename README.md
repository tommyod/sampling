# sampling [![Build Status](https://travis-ci.com/tommyod/sampling.svg?branch=master)](https://travis-ci.com/tommyod/sampling) [![PyPI version](https://badge.fury.io/py/sampling.svg)](https://pypi.org/project/sampling/) [![Documentation Status](https://readthedocs.org/projects/sampling/badge/?version=latest)](https://sampling.readthedocs.io/en/latest/?badge=latest) [![Downloads](https://pepy.tech/badge/sampling)](https://pepy.tech/project/sampling) [![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

An efficient pure Python implementation of sampling with and without replacement, with and without weights. Works with Python 3.6+.

## Getting started
We use an Urn object to represent the collection of objects we want to sample from. A wrapper method is available for simplification. See examples below.

### Example 1 - Four sampling techniques with wrapper
```python
from sampling import sample
data = ['a','b','b','c']
weights = [1., 1.1, 1.5, 2.]
samples_count = 3

# No replacement, no weights
example1 = sample(data, samples_count)

# With replacement, no weights
example2 = sample(data, samples_count, replace=True)

# No replacement, with weights
example3 = sample(data, samples_count, weights=weights)

# With replacement, with weights
example4 = sample(data, samples_count, replace=True, weights=weights)
```

### Example 2 - Four sampling techniques with the Urn object
```python
from sampling import Urn
import itertools

data = [1,2,3,4]
weights = [1.1, 1.2, 1.3, 1.4]
samples_cnt = 3

# No replacement, no weights
urn = Urn(population=data)
example1 = list(itertools.islice(urn, samples_count))

# With replacement, no weights
urn = Urn(data, replace=True)
example2 = list(itertools.islice(urn, samples_count))   

# No replacement, with weights
urn = Urn(data, weights=weights)
example3 = list(itertools.islice(urn, samples_count))

# With replacement, with weights
urn = Urn(data, replace=True, weights=weights)
example4 = list(itertools.islice(urn, samples_count))
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
