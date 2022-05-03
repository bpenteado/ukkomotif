# import sys
# sys.path.append("/Users/bpenteado/ukkomotif")

from ukkomotif import main

import pytest

def test_stringer():
    assert isinstance(main.stringer("hello"), str)
    assert main.stringer("hello") == "hello"
    with pytest.raises(TypeError):
        main.stringer(1.1)
        main.stringer([1])
        main.stringer(1)