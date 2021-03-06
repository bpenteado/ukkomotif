from ukkomotif.ukkonen import SuffixTree

import pytest

def test_suffix_tree():
    test_string_single = "AAATGGCCGCGCCG#"
    test_string_multiple = "AAATGGCCGCGCCG#AAATGGCCGCGCCG#GGCTGTTGAGCGCGCGGGA#"
    
    # tree build tests
    assert (SuffixTree(test_string_single, "#").remainder == 0)
    assert (SuffixTree(test_string_single, "#").count_leaves() == len(test_string_single))
    assert (SuffixTree(test_string_multiple, "#").remainder == 0)
    assert (SuffixTree(test_string_multiple, "#").count_leaves() == len(test_string_multiple))

    with pytest.raises(ValueError):
        SuffixTree(test_string_single[:-1], "#")

    # substring count tests
    assert (SuffixTree(test_string_multiple, "#").count_substring("AAA") == 2)
    assert (SuffixTree(test_string_multiple, "#").count_substring("GAAA") == 0)
    assert (SuffixTree(test_string_multiple, "#").count_substring("GC") == 10)
    assert (SuffixTree(test_string_multiple, "#").count_substring("AAATGGCCGCGCCG") == 2)