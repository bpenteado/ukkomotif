"""Utility for reading and parsing DNA and conservation input sequences"""

class Parser:
    """Parser utility class"""
    def __init__(self):
        self.separation_symbol = "#"
        self.gap_symbol = "-"
        self.conservation_symbol = "*"
        self.dna_valid_symbols = "ATCG" + self.separation_symbol + self.gap_symbol
        self.conservation_valid_symbols = " " + self.separation_symbol + self.conservation_symbol

    def _parse_sequence(self, type: str, sequence:str, valid_symbols: str, separation_symbol: str):
        if sequence[-1] != separation_symbol:
            raise ValueError(f"{type} sequence should end with a separation/termination symbol.")
        for char in sequence:
            if char not in valid_symbols:
                raise ValueError(f"Invalid character in {type} sequence: {char}")            
        return sequence

    
    def read(self, data:str, is_file: bool) -> str:
        """Reads input data and saves it for parsing."""
        if is_file:
            with open(data, 'r') as file:
                sequence = file.read()
        else:
            sequence = data
        
        return sequence

    def parse_dna_sequence(self, sequence):
        """Checks input DNA sequence for valid symbols and termination"""
        return self._parse_sequence("DNA", sequence, self.dna_valid_symbols, self.separation_symbol)

    def parse_conservation_sequence(self, sequence):
        """Checks input conservation sequence for valid symbols and termination"""
        return self._parse_sequence("Conservation", sequence, self.conservation_valid_symbols, self.separation_symbol)

    def parse_dna_conservation(self, dna_seq:str, conservation_seq: str) -> str:
        """Retrieves motif conservation data from dna and conservation sequences for input into a Suffix Tree.

        :param dna_seq: DNA sequences concatenated as a single string and separated by separation_symbol.
        :type dna_seq: str
        :param conservation_seq: Conservation sequences concatenated as a single string and separated by separation_symbol.
            Conservation sequences are composed of conservation_symbol (conserved nucleotides) and spaces (non-conserved 
            nucleotides).
        :type conservation_seq: str

        :raises ValueError: if DNA and conservation sequences are misaligned or have differing lengths.

        :return: returns a single string with all motifs from dna_seq that are conserved. Motifs are concatenated and 
            separated by separation_symbol.
        :rtype: str
        """

        # validate input strings
        dna_seq = self.parse_dna_sequence(dna_seq)
        conservation_seq = self.parse_conservation_sequence(conservation_seq)

        if len(dna_seq) != len(conservation_seq):
            raise ValueError("DNA and conservation strings must be of same length.")

        conserved_motifs, motif = "", ""
        in_motif = False
        for dna, cons in zip(dna_seq, conservation_seq):
            if self.separation_symbol in [dna, cons]:
                if dna != cons:
                    raise ValueError(f"DNA and conservation sequences must be aligned.")
            if dna == self.gap_symbol:
                continue
            if cons == self.conservation_symbol:
                motif += dna
                in_motif = True
            elif in_motif is True:
                motif += self.separation_symbol
                conserved_motifs += motif
                motif = ""
                in_motif = False

        return conserved_motifs
