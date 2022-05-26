from click.testing import CliRunner

import ukkomotif.cli.main as ucli

runner = CliRunner()

def test_frequency():
    _result = runner.invoke(ucli.frequency, "AATG# 0 2")
    assert _result.exit_code == 0
    assert _result.output == "AA 1\nAT 1\nTG 1\n"

def test_conservation():
    _result = runner.invoke(ucli.conservation, "'AAATGGCCGCGCCG#AAATGGCCGCGCCG#GGCTGTTGAGCGCGCGGGA#' '***  *    ** *#***     ***   #*    ***           #' 0 3")
    assert _result.exit_code == 0
    assert _result.output == "AAA 1.0\nTTG 1.0\nGCG 0.2\n"