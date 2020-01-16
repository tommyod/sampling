from sampling import Urn
import random
import pytest


@pytest.mark.parametrize("weights", [None, [1, 2, 3]])
def test_input_equals_output(weights):
    data = list(range(len(weights)))
    urn = Urn(data, replace=False, weights=weights)
    assert set(urn) == set(data)


@pytest.mark.parametrize("weights", [None, [1, 2, 3]])
def test_usage(weights):
    seed = 123
    data = list(range(len(weights)))

    random.seed(seed)
    urn = Urn(data, replace=False, weights=weights)
    samples1 = list(urn)

    random.seed(seed)
    urn = Urn(data, replace=False, weights=weights)
    samples2 = []

    while urn:
        samples2.append(next(urn))

    random.seed(seed)
    urn = Urn(data, replace=False, weights=weights)
    samples3 = []

    for item in urn:
        samples3.append(item)

    assert samples1 == samples2
    assert samples2 == samples3


if __name__ == "__main__":
    import pytest

    pytest.main(args=[".", "--doctest-modules", "-v", "--capture=sys"])
