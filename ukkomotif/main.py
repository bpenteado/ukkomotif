"""Functions for de novo motif discovery based on genome-wide evolutionary signatures."""

from .parser import Parser
from .ukkonen import SuffixTree
from .weeder import Weeder
from typing import Optional

def compute_kmer_frequencies(dna_data: str, is_file: bool, kmer_length: int) -> dict:
    """Retrieves all motifs of a specified length from a DNA sequence and computes their frequencies.

    :param dna_data: input dna sequence. May be provided as a path to text file or in raw format (string with 
        nucleotides).
    :type dna_data: str
    :param is_file: indicates if dna_data is a path to a file. If dna_data is raw data, set this parameter to False.
    :type is_file: bool
    :param kmer_length: motif length of interest.
    :type kmer_length: int

    :return: dictionary with motifs as keys and frequencies as values. Sorted in decresing order of frequency.
    :rtype: dict
    """
    parser = Parser()
    dna_seq = parser.read(dna_data, is_file)
    dna_seq = parser.parse_dna_sequence(dna_seq)
    dna_seq = dna_seq.replace("-", "")
    
    suffix_tree = SuffixTree(dna_seq, parser.separation_symbol)
    kmer_frequencies = Weeder(suffix_tree, kmer_length).patterns

    kmer_frequencies = dict(sorted(kmer_frequencies.items(), key = lambda item: item[1], reverse = True))

    return kmer_frequencies

def compute_kmer_conservation_frequencies(dna_data: str, conservation_data: str, is_file: bool, kmer_length: int) -> dict:
    """Based on conservation sequence, retrieves conserved motifs of a specified length from a DNA sequence and computes 
    their frequencies.

    :param dna_data: input DNA sequence. May be provided as a path to text file or in raw format (string with 
        nucleotides). If raw data is provided, set is_file to False.
    :type dna_data: str
    :param conservation_data: input conservation sequence. May be provided as a path to text file or in raw format (string with 
        conservation symbols).
    :type conservation_data: str
    :param is_file: indicates if dna_data and conservation_data are paths to text files. If dna_data and 
        conservation_data are raw data, set this parameter to False.
    :type is_file: bool
    :param kmer_length: motif length of interest.
    :type kmer_length: int

    :return: dictionary with conserved motifs as keys and frequencies as values. Sorted in decresing order of frequency.
    :rtype: dict
    """
    parser = Parser()
    dna_seq, conservation_seq = parser.read(dna_data, is_file), parser.read(conservation_data, is_file)
    conserved_motifs = parser.parse_dna_conservation(dna_seq, conservation_seq)

    suffix_tree = SuffixTree(conserved_motifs, parser.separation_symbol)
    conserved_kmer_frequencies = Weeder(suffix_tree, kmer_length).patterns

    conserved_kmer_frequencies = dict(sorted(conserved_kmer_frequencies.items(),
                                             key = lambda item: item[1], 
                                             reverse = True))

    return conserved_kmer_frequencies

def compute_kmer_conservations(dna_file: str, conservation_file: str, is_file: bool, kmer_length: int) -> dict:
    """Based on conservation sequence, retrieves conserved motifs of a specified length from a DNA sequence and computes 
    their conservation. Conservation is defined as motif conservation frequency divided by total motif frequency.  

    :param dna_data: input DNA sequence. May be provided as a path to text file or in raw format (string with 
        nucleotides). If raw data is provided, set is_file to False.
    :type dna_data: str
    :param conservation_data: input conservation sequence. May be provided as a path to text file or in raw format (string with 
        conservation symbols).
    :type conservation_data: str
    :param is_file: indicates if dna_data and conservation_data are paths to text files. If dna_data and 
        conservation_data are raw data, set this parameter to False.
    :type is_file: bool
    :param kmer_length: motif length of interest.
    :type kmer_length: int

    :return: dictionary with conserved motifs as keys and conservations as values. Sorted in decresing order of conservation.
    :rtype: dict
    """
    kmer_frequencies = compute_kmer_frequencies(dna_file, is_file, kmer_length)
    conserved_kmer_frequencies = compute_kmer_conservation_frequencies(dna_file, conservation_file, is_file, kmer_length)

    kmer_conservations = {}
    for item in conserved_kmer_frequencies.items():
        kmer_frequency = kmer_frequencies[item[0]]
        kmer_conservation = item[1]/kmer_frequency
        kmer_conservations[item[0]] = kmer_conservation

    kmer_conservations = dict(sorted(kmer_conservations.items(), key = lambda item: item[1], reverse = True))

    return kmer_conservations