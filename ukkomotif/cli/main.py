"""Entrypoints to service functions through a CLI"""

import click

from ukkomotif.main import stringer as _stringer

@click.group("ukkomotif")
def main():
    """Command line toolchain for ukkomotif.
    
    Visit https://github.com/bpenteado/ukkonen-motif to learn more.
    """

@click.command("stringer")
@click.argument("input_string", nargs=1)
def stringer(input_string: str):
    try:
        _stringer(input_string)
    except Exception as e:
        click.secho(f"Unable to filter input string: {str(e)}", fg="red")
        return
    click.secho("Successfully filtered input string!", fg="green")

main.add_command(stringer)