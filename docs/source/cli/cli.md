# CLI Reference

(ukkomotif_frequency)=
## `ukkomotif frequency`

```console
$ ukkomotif frequency DNA_SEQUENCE IS_FILE KMER_LENGTH [--list=10]
```

Retrieves all motifs of a specified length from a DNA sequence and computes their frequencies.

* `DNA_SEQUENCE`: (string) raw dna data or a path to a file with the DNA data. See [data inputs](data_inputs) for formatting information.
* `IS_FILE`: (int) 
    * 0 if `DNA_SEQUENCE` is raw dna data
    * 1 if `DNA_SEQUENCE` is a path to a file
* `KMER_LENGTH`: (int) motif length of interest.
* `--list`: (int, optional) number of motifs to list in output. Defaults to 10.


(ukkomotif_conservation)=
## `ukkomotif conservation`

```console
$ ukkomotif conservation DNA_SEQUENCE CONSERVATION_SEQUENCE IS_FILE KMER_LENGTH [--list=10]
```

Based on conservation sequence, retrieves conserved motifs of a specified length from a DNA sequence and computes their conservation. Conservation is defined as motif conservation frequency divided by total motif frequency.

* `DNA_SEQUENCE`: (string) raw dna data or a path to a file with the DNA data. See [data inputs](data_inputs) for formatting information.
* `DNA_CONSERVATION`: (string) raw dna data or a path to a file with the conservation data. See [data inputs](data_inputs) for formatting information.
* `IS_FILE`: (int) 
    * 0 if `DNA_SEQUENCE` and `CONSERVATION_DATA` are raw data
    * 1 if `DNA_SEQUENCE` and `CONSERVATION_DATA` are paths to files
* `KMER_LENGTH`: (int) motif length of interest.
* `--list`: (int, optional) number of motifs to list in output. Defaults to 10.
