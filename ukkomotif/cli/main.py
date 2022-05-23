"""Entrypoints to service functions through a CLI"""

import click

from ukkomotif.main import compute_kmer_frequencies, compute_kmer_conservations

@click.group("ukkomotif")
def main():
    """Command line toolchain for ukkomotif.
    
    Visit https://github.com/bpenteado/ukkonen-motif to learn more.
    """

@click.command("frequency")
@click.option('--file', default=True, help="True if sequence_data is a file path")
@click.argument("sequence_data", nargs=1)
@click.argument("kmer_length", type = click.INT, nargs=1)
def frequency(sequence_data: str, kmer_length: int, file: bool = True):
    "Computes all motifs of length KMER_LENGTH and in SEQUENCE_DATA."
    try:
        kmer_frequencies = compute_kmer_frequencies(sequence_data, kmer_length, file)
    except Exception as e:
        click.secho(f"Unable to compute motif frequencies: {str(e)}", fg="red")
        return
    click.secho("Successfully computed motif frequencies!", fg="green")

main.add_command(frequency)