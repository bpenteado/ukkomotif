"""
Ukkonen Suffix Tree for motif discovery basen on genome-wide evolutionary signature.
"""

def stringer(a: str) -> str:
    """
    Type filter that raises an error for non-string inputs.

    :param a: input to be filtered.

    :raises TypeError: if a not a string.
    """
    if not isinstance(a, str):
        raise TypeError("Input must be a string")
    return a