"""Entrypoints to service functions through a CLI"""

import click
from itertools import islice

from ..main import compute_kmer_frequencies, compute_kmer_conservations

def _format_dict_to_text(input_dict: dict, n_list: int=10) -> str:
    formatted_text = ""
    if n_list > len(input_dict.items()):
        n_list = len(input_dict.items())
    for item in islice(input_dict.items(), n_list):
        formatted_text += f"{item[0]} {item[1]}\n"
    return formatted_text[:-1]

@click.group("ukkomotif")
def main():
    """Command line toolchain for ukkomotif.
    
    Visit https://github.com/bpenteado/ukkomotif to learn more.
    """

@click.command("frequency", context_settings={'show_default': True})
@click.argument("sequence_data", metavar="SEQUENCE")
@click.argument("is_file", metavar="ISFILE", type=click.INT)
@click.argument("kmer_length", metavar="KLENGTH", type=click.INT)
@click.option("--list", "n_kmers", default=10, type=int, help="Number of kmers to return")
def frequency(sequence_data: str, is_file: int, kmer_length: int, n_kmers: int):
    """Retrieves all motifs of a specified length from a DNA sequence and computes their frequencies.
    
    Visit https://github.com/bpenteado/ukkomotif to learn more.
    """
    try:
        kmer_frequencies = compute_kmer_frequencies(sequence_data, bool(is_file), kmer_length)
    except Exception as e:  # pragma: no cover, general exception handling
        click.secho(f"Unable to compute motif frequencies: {str(e)}", fg="red")
        return
    return_string = _format_dict_to_text(kmer_frequencies, n_kmers)
    click.secho(return_string)

@click.command("conservation", context_settings={'show_default': True})
@click.argument("sequence_data", metavar="SEQUENCE")
@click.argument("conservation_data", metavar="CONSERVATION")
@click.argument("is_file", metavar="ISFILE", type=click.INT)
@click.argument("kmer_length", metavar="KLENGTH", type=click.INT)
@click.option("--list", "n_kmers", default=10, type=int)
def conservation(sequence_data: str, conservation_data: str, is_file: int, kmer_length: int, n_kmers: int):
    """Based on conservation sequence, retrieves conserved motifs of a specified length from a DNA sequence and computes 
    their conservation. Conservation is defined as motif conservation frequency divided by total motif frequency.
    
    Visit https://github.com/bpenteado/ukkomotif to learn more.
    """
    try: 
        kmer_conservations = compute_kmer_conservations(sequence_data, conservation_data, bool(is_file), kmer_length)
    except Exception as e:  # pragma: no cover, general exception handling
        click.secho(f"Unable to compute motif conservations: {str(e)}", fg="red")
        return
    return_string = _format_dict_to_text(kmer_conservations, n_kmers)
    click.secho(return_string)

main.add_command(frequency)
main.add_command(conservation)