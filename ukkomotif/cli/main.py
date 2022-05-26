"""Entrypoints to service functions through a CLI"""

import click
from itertools import islice

from ..main import compute_kmer_frequencies, compute_kmer_conservations

def _format_dict_to_text(input_dict: dict) -> str:
    formatted_text = ""
    for item in islice(input_dict.items(), 10):
        formatted_text += f"{item[0]} {item[1]}\n"
    return formatted_text[:-1]

@click.group("ukkomotif")
def main():
    """Command line toolchain for ukkomotif.
    
    Visit https://github.com/bpenteado/ukkonen-motif to learn more.
    """

@click.command("frequency")
@click.argument("sequence_data", nargs=1)
@click.argument("is_file", type = click.INT, nargs=1)
@click.argument("kmer_length", type = click.INT, nargs=1)
def frequency(sequence_data: str, is_file: int, kmer_length: int):
    """Retrieves all motifs of a specified length from a DNA sequence and computes their frequencies."""
    try:
        kmer_frequencies = compute_kmer_frequencies(sequence_data, bool(is_file), kmer_length)
    except Exception as e:
        click.secho(f"Unable to compute motif frequencies: {str(e)}", fg="red")
        return
    return_string = _format_dict_to_text(kmer_frequencies)
    click.secho(return_string)

@click.command("conservation")
@click.argument("sequence_data", nargs=1)
@click.argument("conservation_data", nargs=1)
@click.argument("is_file", type=click.INT, nargs=1)
@click.argument("kmer_length", type=click.INT, nargs=1)
def conservation(sequence_data: str, conservation_data: str, is_file: int, kmer_length: int):
    """Based on conservation sequence, retrieves conserved motifs of a specified length from a DNA sequence and computes 
    their conservation. Conservation is defined as motif conservation frequency divided by total motif frequency.
    """
    try: 
        kmer_conservations = compute_kmer_conservations(sequence_data, conservation_data, bool(is_file), kmer_length)
    except Exception as e:
        click.secho(f"Unable to compute motif conservations: {str(e)}", fg="red")
        return
    return_string = _format_dict_to_text(kmer_conservations)
    click.secho(return_string)

main.add_command(frequency)
main.add_command(conservation)