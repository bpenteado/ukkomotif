from click.testing import CliRunner

import ukkomotif.cli.main as ucli

runner = CliRunner()

def test_frequency():
    _result = runner.invoke(ucli.frequency, "AATG# 2 --file False")
    assert _result.exit_code == 0
    assert _result.output == "Successfully computed motif frequencies!\n"