import sys
sys.path.append("/Users/bpenteado/ukkomotif")

from ukkomotif.main import stringer, SuffixTree

import pytest

def test_stringer():
    assert isinstance(stringer("hello"), str)
    assert stringer("hello") == "hello"
    with pytest.raises(TypeError):
        stringer(1.1)
        stringer([1])
        stringer(1)

def test_suffix_tree():
    test_string_single = "AAATGGCCGCGCCG#"
    test_string_multiple = "AAATGGCCGCGCCG#AAATGGCCGCGCCG#GGCTGTTGAGCGCGCGGGA#"
    
    # tree build tests
    assert (SuffixTree(test_string_single, "#").remainder == 0)
    assert (SuffixTree(test_string_single, "#")._count_leaves() == len(test_string_single))
    assert (SuffixTree(test_string_multiple, "#").remainder == 0)
    assert (SuffixTree(test_string_multiple, "#")._count_leaves() == len(test_string_multiple))

    with pytest.raises(ValueError):
        SuffixTree(test_string_single[:-1], "#")

    # substring count tests
    assert (SuffixTree(test_string_multiple, "#").count_substring("AAA") == 2)
    assert (SuffixTree(test_string_multiple, "#").count_substring("GAAA") == 0)
    assert (SuffixTree(test_string_multiple, "#").count_substring("GC") == 10)
    assert (SuffixTree(test_string_multiple, "#").count_substring("AAATGGCCGCGCCG") == 2)