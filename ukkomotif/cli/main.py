"""Entrypoints to service functions through a CLI"""

import click

from ukkomotif.main import compute_kmer_frequencies, compute_kmer_conservations

def _format_dict_to_text(input_dict: dict) -> str:
    formatted_text = ""
    for item in input_dict.items():
        formatted_text += f"{item[0]} {item[1]}\n"
    return formatted_text[:-1]

@click.group("ukkomotif")
def main():
    """Command line toolchain for ukkomotif.
    
    Visit https://github.com/bpenteado/ukkonen-motif to learn more.
    """

@click.command("frequency")
@click.option('--file', default=True, help="True if sequence_data is a file path")
@click.argument("sequence_data", nargs=1)
@click.argument("kmer_length", type = click.INT, nargs=1)
def frequency(sequence_data: str, kmer_length: int, file: bool=True):
    "Computes all motifs of length KMER_LENGTH and in SEQUENCE_DATA."
    # try:
    kmer_frequencies = compute_kmer_frequencies(sequence_data, kmer_length, file)
    # except Exception as e:
    #     click.secho(f"Unable to compute motif frequencies: {str(e)}", fg="red")
    #     return
    return_string = _format_dict_to_text(kmer_frequencies)
    click.secho(return_string)

@click.command("conservation")
@click.option('--file', default=True, help="True if sequence_data is a file path")
@click.argument("sequence_data", nargs=1)
@click.argument("conservation_data", nargs=1)
@click.argument("kmer_length", type=click.INT, nargs=1)
def conservation(sequence_data, conservation_data, kmer_length, file: bool=True):
    try:
        kmer_conservations = compute_kmer_conservations(sequence_data, conservation_data, kmer_length, file)
    except Exception as e:
        click.secho(f"Unable to compute motif conservations: {str(e)}", fg="red")
        return
    return_string = _format_dict_to_text(kmer_conservations)
    click.secho(return_string)

main.add_command(frequency)
main.add_command(conservation)