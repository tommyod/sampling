from sampling import Urn, sample
import itertools
import random
import pytest


class TestUrn:
    @pytest.mark.parametrize("weights", [None, [1, 2, 3]])
    def test_input_equals_output(self, weights):
        """Test that the set of values returned from the urn are the same as the input population:
         - With a non-weighted population
         - With a weighted population
        """
        data = [1, 2, 3]
        urn = Urn(data, replace=False, weights=weights)
        assert set(urn) == set(data)

    @pytest.mark.parametrize("weights", [None, [1, 2, 3]])
    def test_urn_bool(self, weights):
        """Test that bool(urn) works as expected.
        """
        data = [1, 2, 3]
        urn = Urn(data, replace=False, weights=weights)
        assert urn
        assert bool(urn)
        while urn:
            next(urn)
        assert urn.size() == 0
        assert not urn
        assert not bool(urn)

    @pytest.mark.parametrize("weights", [None, [1, 2, 3]])
    def test_urn_length_without_replacement(self, weights):
        """Test that urn.size() works as expected.
        """
        data = [1, 2, 3]
        urn = Urn(data, replace=False, weights=weights)
        assert urn.size() == 3
        next(urn)
        assert urn.size() == 2
        list(urn)  # Exhaust the iterator
        assert urn.size() == 0

    @pytest.mark.parametrize("weights", [None, [1, 2, 3]])
    def test_urn_length_with_replacement(self, weights):
        """Test that urn.size() works as expected.
        """
        data = [1, 2, 3]
        urn = Urn(data, replace=True, weights=weights)
        assert urn.size() == float("inf")

        # Drawing a sample does not change the size
        next(urn)
        assert urn.size() == float("inf")

        # Drawing 50 samples does not change the size
        list(itertools.islice(urn, 50))
        assert urn.size() == float("inf")

    @pytest.mark.parametrize("type_func, replace", list(itertools.product((list, set, tuple, str), (True, False))))
    def test_input_types_unweighted(self, type_func, replace):
        """Test that common Python types work."""
        data = type_func("abcdef")
        urn = Urn(data, replace=replace, weights=None)
        next(urn)

    @pytest.mark.parametrize("type_func, replace", list(itertools.product((list, tuple), (True, False))))
    def test_input_types_weighted(self, type_func, replace):
        """Test that common Python types work."""
        data = type_func("abcdef")
        weights = type_func(i + 1 for i in range(len(data)))
        urn = Urn(data, replace=replace, weights=weights)
        next(urn)

    @pytest.mark.parametrize("weights", [None, [1, 2, 3]])
    def test_usage(self, weights):
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

    def test_list_extension(self):
        """Test the extend method"""
        data = "abcdef"
        urn = Urn(data, replace=False)
        assert urn.size() == 6
        urn.extend("xy")
        assert urn.size() == 8

    @pytest.mark.parametrize("replace", [True, False])
    def test_list_extension_stochastic(self, replace):
        """Test the extend method"""
        data = "abcdef"
        urn = Urn(data, replace=replace)
        urn.extend("xy")
        assert set(["x", "y"]).issubset(set(itertools.islice(urn, 1000)))

    def test_contains_unweighted_infinite(self):
        """Test the __contains__ method"""
        data = "abcdef"
        urn = Urn(data, replace=True)
        # Draw one sample, then verify that everything is still in the urn
        next(urn)
        for element in data:
            assert element in urn

    def test_contains_unweighted_finite(self):
        """Test the __contains__ method"""
        data = "abcdef"
        urn = Urn(data, replace=False)
        # Draw one sample, then verify that element is not still in the urn
        for element in urn:
            assert element not in urn

    def test_remove(self):
        """Test the __contains__ method"""
        data = "abcdef"
        to_remove = "bcd"
        urn = Urn(data, replace=False)
        # Draw one sample, then verify that element is not still in the urn
        for element in to_remove:
            assert element in urn
            urn.remove(element)
            assert element not in urn

    @pytest.mark.parametrize("replace", [True, False])
    def test_add_weighted(self, replace):
        data = "acf"
        weights = [1, 2, 3]
        more_data = "bde"
        more_weights = [4, 5, 6]
        urn = Urn(data, replace, weights)
        for element, weight in zip(more_data, more_weights):
            assert element not in urn
            urn.add(element, weight)
            assert element in urn
        assert urn.size() == 6 or urn.size() == float("inf")

    @pytest.mark.parametrize("replace", [True, False])
    def test_remove_weighted(self, replace):
        data = "abcdef"
        weights = [1, 2, 3, 4, 5, 6]
        to_remove = "bde"
        urn = Urn(data, replace, weights)
        for element in to_remove:
            assert element in urn
            urn.remove(element)
            assert element not in urn
        assert urn.size() == 3 or urn.size() == float("inf")


class TestSampleFunction:
    @pytest.mark.parametrize("k", [1, 5, 25])
    def test_api(self, k):
        """Test basic API for sample function."""

        data = list(range(100))
        data_in = data.copy()
        sampled_elements = sample(data)
        assert data == data_in  # Function does not change the data
        assert isinstance(sampled_elements, list)
        assert len(sampled_elements) == 1
        assert set(sampled_elements).issubset(set(data))
