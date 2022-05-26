from ukkomotif.main import compute_kmer_frequencies, compute_kmer_conservation_frequencies, compute_kmer_conservations

import pytest
import re

sample_sequence_data = "AAATGGCCGCGCCG--#AAA---TGGC----CGCGCCG#GGCTGTTGAGCGCGCGG-GA#"
sample_conservation_data = "***  *    ** ***#***            ***   #*    ***            #"

full_sequence_file = "tests/allinter"
full_conservation_file = "tests/allintercons"

def test_compute_kmer_frequencies():
    kmer_frequencies = compute_kmer_frequencies(sample_sequence_data, 3, False)
    assert len(kmer_frequencies) == 20
    assert kmer_frequencies['AAA'] == 2
    assert kmer_frequencies['GGA'] == 1
    with pytest.raises(KeyError):
        assert kmer_frequencies["GAA"]
    with pytest.raises(FileNotFoundError):
        assert compute_kmer_frequencies(sample_sequence_data, 3)

    with open(full_sequence_file, "r") as file:
        full_sequence_data = file.read()
    
    kmer_frequencies = compute_kmer_frequencies(full_sequence_file, 3)
    assert kmer_frequencies['AAA'] == len(re.findall('(?=AAA)', full_sequence_data.replace("-","")))
    assert kmer_frequencies['TGC'] == len(re.findall('(?=TGC)', full_sequence_data.replace("-","")))
    assert not any("-" in kmer for kmer in kmer_frequencies.keys())

def test_compute_kmer_conservation_frequencies():
    kmer_conservation_frequencies = compute_kmer_conservation_frequencies(sample_sequence_data, sample_conservation_data, 3, False)
    assert len(kmer_conservation_frequencies) == 3
    assert kmer_conservation_frequencies["AAA"] == 2
    assert kmer_conservation_frequencies["GCG"] == 1
    assert kmer_conservation_frequencies["TTG"] == 1
    assert not any("-" in kmer for kmer in kmer_conservation_frequencies.keys())
    with pytest.raises(KeyError):
        assert kmer_conservation_frequencies["GAA"]

def test_compute_kmer_conservations():
    kmer_conservations = compute_kmer_conservations(sample_sequence_data, sample_conservation_data, 3, False)
    assert len(kmer_conservations) == 3
    assert kmer_conservations["AAA"] == 1
    assert kmer_conservations["GCG"] == 0.2
    assert kmer_conservations["TTG"] == 1