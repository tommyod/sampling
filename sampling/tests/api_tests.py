from sampling import Urn
import random
import pytest


@pytest.mark.parametrize("weights", [None, [1, 2, 3]])
def test_input_equals_output(weights):
    """Test that the set of values returned from the urn are the same as the input population:
     - With a non-weighted population
     - With a weighted population
    """
    data = [1, 2, 3]
    urn = Urn(data, replace=False, weights=weights)
    assert set(urn) == set(data)


@pytest.mark.parametrize("weights", [None, [1, 2, 3]])
def test_usage(weights):
    """Test that usage functionality of the urn is equivalent:
     - Cast to list directly
     - Iterate with a while loop and add to list
     - For loop the Urn
    """
    seed = 123
    data = [1, 2, 3]

    random.seed(seed)
    urn = Urn(data, replace=False, weights=weights)
    assert len(urn) == 3
    samples1 = list(urn)
    assert len(urn) == 0

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

    assert samples1 == samples3
    assert samples2 == samples3
