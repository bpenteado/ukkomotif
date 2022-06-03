# ukkomotif

![build](https://github.com/bpenteado/ukkomotif/actions/workflows/build.yml/badge.svg) [![coverage](https://codecov.io/gh/bpenteado/ukkomotif/branch/main/graph/badge.svg?token=IEAQUAHQ68)](https://codecov.io/gh/bpenteado/ukkomotif) [![docs](https://readthedocs.org/projects/ukkomotif/badge/?version=latest)](https://ukkomotif.readthedocs.io/en/latest/?badge=latest)

Discovery of functional genomic motifs using Ukkonen's implementatin of a suffix tree and the Weeder algorithm.

## Why Ukkomotif

Motifs that are evolutionarily conserved in the genome are high-potential candidates for relevant genomic functionality.

Ukkomotif is a modular toolchain for the discovery of functional genomic motifs using genome-wide evolutionary signatures. It allows users to compute the frequency and conservation of kmers (motifs) of any length by providing genomic sequences together with their conservation signatures.

Functionality is provided through CLI and functional endpoints.

Ukkomotif also provides standalone services for the implementation and manipulation of suffix trees built with Ukkonen's algorithm.


## Core Components

![components](static/components.png)

- **main.py**: defines functional endpoints.
    * **computer_kmer_frequency()**: given a DNA sequence and a specified motif length, retrieves all motifs and their frequencies.
    * **compute_kmer_conservation()**: given a DNA sequence, a conservation sequence, and a specified motif length, retrieves all conserved motifs and their conservation. Conservation is defined as motif conservation frequency divided by total motif frequency.
- **cli/main.py**: defines command line endpoints.
    * **ukkomotif frequency**: CLI endpoint for compute_kmer_frequency()
    * **ukkomotif conservation**: CLI endpoint for compute_kmer_conservation()
- **parser.py**: verifies and sanitizes raw user data.
- **ukkonen.py**: suffix tree implementation based on Ukkonen's online algorithm.
- **weeder.py**: Wedder algorithm implementation. Given a suffix tree and a substring length, finds all substrings of the specific length and computes their frequency.

## Usage

To calculate motif frequencies using the CLI, use `ukkomotif frequency`.
```console
$ ukkomotif frequency "AAAGCCCCG--#AA---TGGC--CGCGCCG#GGCAGCGC-GA#" 0 3 --list 5
GCC 3
GCG 3
CCG 3
CGC 3
AGC 2
$ ukkomotif frequency PATH_TO_DNA 1 4 --list 3
AAAA 70931
TTTT 69711
ATAT 42771
```

To calculate motif conservations using the CLI, use `ukkomotif conservation`:
```console
$ ukkomotif conservation "ATCG--#AAAT#" " ** **# ***#" 0 2 --list 3
TC 1.0
AA 0.5
AT 0.5
$ ukkomotif conservation PATH_TO_DNA PATH_TO_CONSERVATION 1 6 --list 5
TACCCG 0.4327731092436975
CGGGTA 0.43243243243243246
CCGGGT 0.38524590163934425
ACCCGG 0.36860068259385664
CACGTG 0.3489010989010989
```

To calculate motif frequencies and conservations using the functional endpoints:
```python
from ukkomotif.main import compute_kmer_frequency, compute_kmer_conservation

# using raw data
sequence = "AAAGCCCCG--#AA---TGGC--CGCGCCG#GGCTGTAGCGC-GA#"
conservation= "***   **  *#**  *   ***   * * #*      ****  *#"
kmer_frequencies = compute_kmer_frequency(sequence, False, 3)
kmer_conservations = compute_kmer_conservation(sequence, conservation, False, 3)

# using data in files
seq_path = "tests/allinter"
cons_path = "tests/allintercons"
frequencies = compute_kmer_frequency(seq_path, True, 3)
conservations = compute_kmer_conservation(seq_path, cons_path, True, 3)
```

To build a suffix tree, use `SuffixTree` from the ukkonen module:
```python
from ukkomotif.ukkonen import SuffixTree

string = "AGTAGGT#TAGATCCGC#CTCGCGC#"
tree = SuffixTree(string, "#")
```

## Data Inputs

Users need to provide a `dna_sequence` and a `conservation_sequence`.
- `dna_sequence`: single string with genomic sequences separated by "#". 
    * Valid characters: "ATCG-#"
- `conservation_sequence`: single string with conservation sequences separated by "#". An asterisk "*" marks a conserved nucleotide and a space " " marks a non-conserved nucleotide.
    * Valid character: " *#"
- `dna_sequence` and `conservation_sequence` need to be aligned and of same length.
- Ukkomotif verifies inputs and raises errors in case of badly formatted inputs.

## Getting Started

To begin wrangling DNA, simply:
```console
$ python3 -m pip install ukkomotif
```