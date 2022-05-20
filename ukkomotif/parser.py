"""Reads input files with DNA sequences or conservation patterns and parses data."""

from typing import Tuple

def read(dna_file:str , conservation_file: str = None) -> Tuple:
    """
    Reads input files and saves data for parsing.

    :param dna_seq: path to file with DNA sequences concatenated as a single string and separated by separation_symbol.
    :type dna_seq: str
    :param conservation_seq: path to file with conservation sequences concatenated as a single string and separated by
        separation_symbol. Conservation sequences are composed of conservation_symbol (conserved nucleotides) and spaces 
        (non-conserved nucleotides). Must be of same length as data in dna_file, defaults to None.
    :type dna_seq: str, optional

    :raises ValueError: If both DNA and conservation files are provided, raises error if their data differ in length.

    :return: tuple (data in DNA file, data in conservation file). If conservation file is not provided, data in 
        conservation file is set to None.
    :rtype: tuple

    """
    with open(dna_file, 'r') as dna_data:
        dna_seq = dna_data.read()
    
    if conservation_file == None:
        return (dna_seq, None)
    
    with open(conservation_file, 'r') as conservation_data:
        conservation_seq = conservation_data.read()

    if len(dna_seq) != len(conservation_seq):
        raise ValueError("Data in DNA and conservation files must be of same length.")

    return (dna_seq, conservation_seq)

def parse(dna_seq:str , conservation_seq: str = None, separation_symbol: str = "#", conservation_symbol: str = "*") -> str:
    """
    Parses data for input into a Suffix Tree.

    :param dna_seq: DNA sequences concatenated as a single string and separated by separation_symbol.
    :type dna_seq: str
    :param conservation_seq: Conservation sequences concatenated as a single string and separated by separation_symbol.
        Conservation sequences are composed of conservation_symbol (conserved nucleotides) and spaces (non-conserved 
        nucleotides). Must be of same length as string in dna_seq, defaults to None.
    :type dna_seq: str, optional
    :param separation_symbol: character used to separate DNA and conservation sequences in input files, defaults to "#".
    :type separation_symbol: str, optional
    :param conservation_symbol: character used to tag conserved nucleotides in conservation_seq, defaults to "*".
    :type conservation_symbol: str, optional

    :raises ValueError: If both DNA and conservation strings are provided, raises error if they are of different lengths
        or if sequences are misaligned.

    :return: If conservation_seq is not provided, returns dna_seq. If conservation_seq is provided, returns all motifs 
        from dna_seq that are conserved, separated by separation_symbol.
    :rtype: str
    """
    
    if len(dna_seq) != len(conservation_seq):
        raise ValueError("DNA and conservation strings must be of same length.")

    conserved_motifs, motif = "", ""
    in_motif = False
    for dna, cons in zip(dna_seq, conservation_seq):
        if dna not in ["A", "T", "C", "G", separation_symbol]:
            raise ValueError(f"Invalid character in DNA sequence: {dna}")
        if cons not in [" ", conservation_symbol, separation_symbol]:
            raise ValueError(f"Invalid character in conservation sequence: {cons}")
        if separation_symbol in [dna, cons]:
            if dna != cons:
                raise ValueError(f"DNA and conservation sequences must be aligned.")
        if cons == conservation_symbol:
            motif += dna
            in_motif = True
        elif in_motif is True:
            motif += separation_symbol
            conserved_motifs += motif
            motif = ""
            in_motif = False

    return conserved_motifs
