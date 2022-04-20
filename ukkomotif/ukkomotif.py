"""
Ukkonen Suffix Tree for motif discovery basen on genome-wide evolutionary signature.
"""
import sys

print(sys.path)

def main(a: str) -> str:
    if not isinstance(a, str):
        raise TypeError("Input must be a string")
    return a