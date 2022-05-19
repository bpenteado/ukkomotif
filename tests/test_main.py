import sys
sys.path.append("/Users/bpenteado/ukkomotif")

from ukkomotif.main import stringer, SuffixTree
from ukkomotif.weeder import Weeder

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

def test_weeeder():
    test_string_single = "AAATGGCCGCGCCG#"
    test_string_multiple = "AAATGGCCGCGCCG#AAATGGCCGCGCCG#GGCTGTTGAGCGCGCGGGA#"

    assert len(Weeder(SuffixTree("banana#", "#"), 2).patterns) == 3

    weeder_patterns_single = Weeder(SuffixTree(test_string_single, "#"), 2).patterns   
    assert weeder_patterns_single["AA"] == 2
    with pytest.raises(KeyError):
        assert weeder_patterns_single["AG"]
        assert weeder_patterns_single["AAA"]
        assert weeder_patterns_single["#"]

    weeder_patterns_multiple = Weeder(SuffixTree(test_string_multiple, "#"), 2).patterns   
    assert weeder_patterns_multiple["AA"] == 4
    with pytest.raises(KeyError):
        assert weeder_patterns_multiple["AG"]
        assert weeder_patterns_multiple["AAA"]
        assert weeder_patterns_multiple["#"]