from .parser import Parser
from .ukkonen import SuffixTree
from .weeder import Weeder

def compute_kmer_frequency(dna_file: str, kmer_length: int):
    parser = Parser()
    dna_seq = parser.read(dna_file)
    dna_seq = parser.parse_dna_sequence(dna_seq)
    
    suffix_tree = SuffixTree(dna_seq, parser.separation_symbol)
    kmer_frequencies = Weeder(suffix_tree, kmer_length).patterns
    
    return kmer_frequencies

def compute_kmer_conservation(dna_file: str, conservation_file: str, kmer_length: int):
    parser = Parser()
    dna_seq, conservation_seq = parser.read(dna_file), parser.read(conservation_file)
    conserved_motifs = parser.parse_dna_conservation(dna_seq, conservation_seq)

    suffix_tree = SuffixTree(conserved_motifs, parser.separation_symbol)
    conserved_kmer_frequencies = Weeder(suffix_tree, kmer_length).patterns

    return conserved_kmer_frequencies