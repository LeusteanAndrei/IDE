def test_algorithms_dict_structure():
    from algorithms import INSERTION_SORT, QUICK_SORT, MERGE_SORT, BINARY_SEARCH, LINEAR_SEARCH, LINKED_LIST, STACK, QUEUE, DIJKSTRA, FLOYD_WARSHALL, KNAPSACK, PRIME_CHECK, GCD

    assert "template <typename T>" in INSERTION_SORT
    assert "template <typename T>" in QUICK_SORT
    assert "template <typename T>" in MERGE_SORT
    assert "template <typename T>" in BINARY_SEARCH
    assert "template <typename T>" in LINEAR_SEARCH
    assert "template <typename T>" in LINKED_LIST
    assert "template <typename T>" in STACK
    assert "template <typename T>" in QUEUE
    assert "template <typename T>" in DIJKSTRA
    assert "template <typename T>" in FLOYD_WARSHALL
    assert "template <typename T>" in KNAPSACK
    assert "template <typename T>" in PRIME_CHECK
    assert "template <typename T>" in GCD


import re

def test_all_algorithms_are_templates():
    import algorithms
    template_pattern = re.compile(r"template\s*<\s*typename\s+T\s*>")
    # List all algorithm variables you want to check
    algo_vars = [
        'INSERTION_SORT', 'QUICK_SORT', 'MERGE_SORT', 'BINARY_SEARCH', 'LINEAR_SEARCH',
        'LINKED_LIST', 'STACK', 'QUEUE', 'DIJKSTRA', 'FLOYD_WARSHALL', 'KNAPSACK', 'PRIME_CHECK', 'GCD'
    ]
    for name in algo_vars:
        code = getattr(algorithms, name)
        assert template_pattern.search(code), f"{name} does not have a template declaration"