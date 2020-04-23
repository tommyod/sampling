from sampling.tree import CumulativeSumTree
import random
import math
import pytest


@pytest.mark.parametrize("num_weights", [10, 100, 1000])
def test_query(num_weights):
    """Test that:
     - The sum of weights to the left of the returned index is smaller
        than the query weight
     - The sum of weights to the left of the return index + the weight
        associated with the index is greater than the query weight
    """

    random.seed(42)
    weights = [random.random() for _ in range(num_weights)]
    tree = CumulativeSumTree(weights)
    for _ in range(num_weights):
        weight = random.random() * tree.get_sum()
        i = tree.query(weight)
        assert 0 <= i <= num_weights - 1
        left_sum = sum(tree[j] for j in range(len(weights)) if j < i)
        assert left_sum < weight
        assert left_sum + tree[i] >= weight


@pytest.mark.parametrize("num_weights", [100, 1000, 10000])
def test_setting_weights_to_zero(num_weights):
    """Test that:
     - The indices returned are unique
    """

    weights = [random.random() for _ in range(num_weights)]
    # Realign weights for greater diff
    weights = [-math.log(w) for w in weights]
    indices = []

    tree = CumulativeSumTree(weights)
    for _ in range(num_weights):
        weight = random.random() * tree.get_sum()
        i = tree.query(weight)
        indices.append(i)
        tree.update_weight(i, 0)

    assert len(indices) == len(set(indices))


@pytest.mark.parametrize("scale", [1e25, 1e-25])
def test_scale_invariance_of_weights(scale):
    """Test that:
     - Sampling is invariant when multiplied with a large or small constant
    """

    def sample_indices(scale):
        random.seed(42)
        num_weights = 100
        weights = [scale * random.random() for _ in range(num_weights)]

        tree = CumulativeSumTree(weights)
        for _ in range(num_weights):
            weight = random.random() * tree.get_sum()
            i = tree.query(weight)
            tree.update_weight(i, 0)
            yield i

    assert list(sample_indices(1)) == list(sample_indices(scale))
