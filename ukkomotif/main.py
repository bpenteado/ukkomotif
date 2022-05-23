from .parser import Parser
from .ukkonen import SuffixTree
from .weeder import Weeder
from typing import Optional

def compute_kmer_frequencies(dna_data: str, kmer_length: int, is_file: Optional[bool] = True) -> dict:
    parser = Parser()
    dna_seq = parser.read(dna_data, is_file)
    dna_seq = parser.parse_dna_sequence(dna_seq)
    
    suffix_tree = SuffixTree(dna_seq, parser.separation_symbol)
    kmer_frequencies = Weeder(suffix_tree, kmer_length).patterns
    
    kmer_frequencies = dict(sorted(kmer_frequencies.items(), key = lambda item: item[1], reverse = True))

    return kmer_frequencies

def compute_kmer_conservation_frequencies(dna_data: str, conservation_data: str, kmer_length: int, is_file: Optional[bool] = True) -> dict:
    parser = Parser()
    dna_seq, conservation_seq = parser.read(dna_data, is_file), parser.read(conservation_data, is_file)
    conserved_motifs = parser.parse_dna_conservation(dna_seq, conservation_seq)

    suffix_tree = SuffixTree(conserved_motifs, parser.separation_symbol)
    conserved_kmer_frequencies = Weeder(suffix_tree, kmer_length).patterns

    conserved_kmer_frequencies = dict(sorted(conserved_kmer_frequencies.items(),
                                             key = lambda item: item[1], 
                                             reverse = True))

    return conserved_kmer_frequencies

def compute_kmer_conservations(dna_file: str, conservation_file: str, kmer_length: int, is_file: Optional[bool] = True) -> dict:
    kmer_frequencies = compute_kmer_frequencies(dna_file, kmer_length, is_file)
    kmer_conservation_frequencies = compute_kmer_conservation_frequencies(dna_file, conservation_file, kmer_length, is_file)

    kmer_conservations = {}
    for item in kmer_conservation_frequencies.items():
        kmer_frequency = kmer_frequencies[item[0]]
        kmer_conservation = item[1]/kmer_frequency
        kmer_conservations[item[0]] = kmer_conservation

    kmer_conservations = dict(sorted(kmer_conservations.items(), key = lambda item: item[1], reverse = True))

    return kmer_conservations