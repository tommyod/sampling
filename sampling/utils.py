from sampling.urns import Urn
import itertools


def sample(population, size=1, replace=False, weights=None):
    """
    Draw samples from a collection.
    
    Parameters
    ----------
    population: list
        The data points. 
    
    replace: bool
        Sample with or without replacement.
        
    weights: list
        One weight per data point. If None is
        passed, uniform weights are used.
        
    Returns
    -------
    list
    Returns a new list of length size containing elements from the population 
    while leaving the original population unchanged.
        
        
    Examples
    --------
    >>> data = [1, 3, 4, 7]
    >>> weights = [3, 4, 2, 1]
    >>> sample(data, replace=False, weights=weights)
    >>> sample(data, replace=False, weights=None)
    
    """
    urn = Urn(population=population, replace=replace, weights=weights)
    return list(itertools.islice(urn, size))


def permute(population):
    """Randomly permute the population."""
    return list(Urn(population=population, replace=False, weights=None))
