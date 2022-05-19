import sys
sys.path.append("/Users/bpenteado/ukkomotif")

from ukkomotif.weeder import Weeder
from ukkomotif.ukkonen import SuffixTree

import pytest

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