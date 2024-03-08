import itertools


CORRECT = 'Y'
WRONG_POSITION = '?'
INCORRECT = 'N'

ALL_STATUSES = {CORRECT, WRONG_POSITION, INCORRECT}


def cartesian_product_general(collections: list[list]) -> list[list]:
    """Returns the Cartesian product of the given collections.

    Preconditions:
    - collections != []

    >>> list0 = [1, 2, 3]
    >>> list1 = [10, 20]
    >>> list2 = [100, 200]
    >>> cartesian_product_general([list0, list1])  # This is the familiar Cartesian product with 2 collections
    [[1, 10], [1, 20], [2, 10], [2, 20], [3, 10], [3, 20]]
    >>> result = cartesian_product_general([list0, list1, list2])  # Now, all combinations across 3 collections
    >>> import pprint
    >>> pprint.pprint(result)  # We didn't have to use this library, but it makes the output a bit more readable
    [[1, 10, 100],
     [1, 10, 200],
     [1, 20, 100],
     [1, 20, 200],
     [2, 10, 100],
     [2, 10, 200],
     [2, 20, 100],
     [2, 20, 200],
     [3, 10, 100],
     [3, 10, 200],
     [3, 20, 100],
     [3, 20, 200]]
    """
    return [list(x) for x in itertools.product(*collections)]