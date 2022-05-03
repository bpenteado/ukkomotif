# import sys
# sys.path.append("/Users/bpenteado/ukkomotif")

from click.testing import CliRunner

import ukkomotif.cli.main as ucli

runner = CliRunner()

def test_stringer():
    _result = runner.invoke(ucli.stringer, "hello")
    assert _result.exit_code == 0
    assert _result.output == "Successfully filtered input string!\n"

    _result2 = runner.invoke(ucli.stringer, 1)
    assert _result2.output != "Successfully filtered input string!\n"