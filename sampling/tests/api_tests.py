from sampling import Urn
import random
import pytest


@pytest.mark.parametrize("weights", [None, None])
def test_input_equals_output(weights):
    data = [1, 2, 3]
    urn = Urn(data, replace=False, weights=weights)
    assert set(urn) == set(data)


@pytest.mark.parametrize("weights", [None, None])
def test_usage(weights):
    seed = 123
    data = [1, 2, 3]

    random.seed(seed)
    urn = Urn(data, replace=False, weights=weights)
    samples1 = list(urn)

    # random.seed(seed)
    # urn = Urn(data, replace=False, weights=weights)
    # samples2 = []

    # while urn:
    #   samples2.append(next(urn))

    random.seed(seed)
    urn = Urn(data, replace=False, weights=weights)
    samples3 = []

    for item in urn:
        print(item)
        samples3.append(item)

    assert samples1 == samples3
    # assert samples2 == samples3


if __name__ == "__main__":
    import pytest

    pytest.main(args=[__file__, "--doctest-modules", "-v", "--capture=sys"])
