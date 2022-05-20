import sys
sys.path.append("/Users/bpenteado/ukkomotif")

from ukkomotif.parser import read, parse

import pytest

def test_parse():
    with pytest.raises(ValueError):
        assert parse("ATCG#AAT#GCGGC#", " ** #   #***** #")  # differing lengths
        assert parse("ATCG#AAT#GCGGC#", " ** #   *#****#")  # misaligned sequences
        assert parse("ATCG#AAT!GCGGC#", " ** #   #*****#")  # invalid dna sequence
        assert parse("ATCG#ABT#GCGGC#", " ** #   #*****#")  # invalid dna sequence
        assert parse("ATCG#AAT#GCGGC#", " ** #   #**A**#")  # invalid conservation sequence
        assert parse("ATCG#AAT#GCGGC#", " ** !   #*****#")  # invalid conservation sequence

    assert parse("ATCG#AAT#GCGGC#", " ** #   #*****#") == "TC#GCGGC#"
    assert parse("ATCG#AAT#GCGGC#", " ** #  *#**   #") == "TC#T#GC#"
    