"""
Ukkonen Suffix Tree for motif discovery basen on genome-wide evolutionary signature.
"""

def stringer(input_string: str) -> str:
    """
    Type filter that raises an error for non-string inputs.

    :param input_string: input to be filtered.

    :raises TypeError: if input_string is not a string.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    return input_string