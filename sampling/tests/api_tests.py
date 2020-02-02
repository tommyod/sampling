from sampling import Urn
import itertools
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
def test_urn_bool(weights):
    """Test that bool(urn) works as expected.
    """
    data = [1, 2, 3]
    urn = Urn(data, replace=False, weights=weights)
    assert urn
    assert bool(urn)
    while urn:
        next(urn)
    assert len(urn) == 0
    assert not urn
    assert not bool(urn)


@pytest.mark.parametrize("weights", [None, [1, 2, 3]])
def test_urn_length_without_replacement(weights):
    """Test that len(urn) works as expected.
    """
    data = [1, 2, 3]
    urn = Urn(data, replace=False, weights=weights)
    assert len(urn) == 3
    next(urn)
    assert len(urn) == 2
    list(urn)  # Exhaust the iterator
    assert len(urn) == 0


@pytest.mark.parametrize("weights", [None, [1, 2, 3]])
def test_urn_length_with_replacement(weights):
    """Test that len(urn) works as expected.
    """
    data = [1, 2, 3]
    urn = Urn(data, replace=True, weights=weights)
    assert len(urn) == float("inf")

    # Drawing a sample does not change the length
    next(urn)
    assert len(urn) == float("inf")

    # Drawing 50 samples does not change the length
    list(itertools.islice(urn, 50))
    assert len(urn) == float("inf")


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

    assert samples1 == samples3
    assert samples2 == samples3
