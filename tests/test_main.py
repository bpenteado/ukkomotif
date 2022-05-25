from ukkomotif.main import compute_kmer_frequencies, compute_kmer_conservation_frequencies, compute_kmer_conservations

import pytest

test_sequence_data = "AAATGGCCGCGCCG--#AAA---TGGC----CGCGCCG#GGCTGTTGAGCGCGCGG-GA#"
test_conservation_data = "***  *    ** *  #***            ***   #*    ***            #"

def test_compute_kmer_frequencies():
    kmer_frequencies = compute_kmer_frequencies(test_sequence_data, 3, False)
    assert len(kmer_frequencies) == 32
    assert kmer_frequencies['AAA'] == 2
    with pytest.raises(KeyError):
        assert kmer_frequencies["GAA"]
    with pytest.raises(FileNotFoundError):
        assert compute_kmer_frequencies(test_sequence_data, 3)

def test_compute_kmer_conservation_frequencies():
    kmer_conservation_frequencies = compute_kmer_conservation_frequencies(test_sequence_data, test_conservation_data, 3, False)
    assert len(kmer_conservation_frequencies) == 3
    assert kmer_conservation_frequencies["AAA"] == 2
    assert kmer_conservation_frequencies["GCG"] == 1
    assert kmer_conservation_frequencies["TTG"] == 1
    with pytest.raises(KeyError):
        assert kmer_conservation_frequencies["GAA"]

def test_compute_kmer_conservations():
    kmer_conservations = compute_kmer_conservations(test_sequence_data, test_conservation_data, 3, False)
    assert len(kmer_conservations) == 3
    assert kmer_conservations["AAA"] == 1
    assert kmer_conservations["GCG"] == 0.2
    assert kmer_conservations["TTG"] == 1
