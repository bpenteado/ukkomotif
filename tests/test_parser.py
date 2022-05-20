from ukkomotif.parser import Parser

import pytest

def test_parse():
    parser = Parser()
    with pytest.raises(ValueError):
        assert parser.parse_dna_conservation("ATCG#AAT#GCGGC#", " ** #   #***** #")  # differing lengths
        assert parser.parse_dna_conservation("ATCG#AAT#GCGGC#", " ** #   *#****#")  # misaligned sequences
        assert parser.parse_dna_conservation("ATCG#AAT!GCGGC#", " ** #   #*****#")  # invalid dna sequence
        assert parser.parse_dna_conservation("ATCG#ABT#GCGGC#", " ** #   #*****#")  # invalid dna sequence
        assert parser.parse_dna_conservation("ATCG#AAT#GCGGC#", " ** #   #**A**#")  # invalid conservation sequence
        assert parser.parse_dna_conservation("ATCG#AAT#GCGGC#", " ** !   #*****#")  # invalid conservation sequence

    assert parser.parse_dna_conservation("ATCG#AAT#GCGGC#", " ** #   #*****#") == "TC#GCGGC#"
    assert parser.parse_dna_conservation("ATCG#AAT#GCGGC#", " ** #  *#**   #") == "TC#T#GC#"
    