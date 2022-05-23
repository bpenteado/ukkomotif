"""Weeder algorithm"""

from .ukkonen import SuffixTree, Node
from typing import Optional

class Weeder:
    """
    Computes all kmers of length kmer_length in the Suffix tree, together with their counts.

    :param tree: suffix tree built from some input data.
    :param kmer_length: length of kmers to return.
    """
    def __init__(self, tree: SuffixTree, kmer_length: int):
        self.tree = tree
        self.kmer_length = kmer_length
        self.patterns = {}
        self._run(self.tree, self.tree.root, self.kmer_length, "")

    def _run(self, tree: SuffixTree, start_node: Node, kmer_length: int, path: str):
        """Implements the Weeder algorithm through a depth-first traversal of the tree."""
        for edge in start_node.edges:
            if tree.string[edge.start] == tree.symbol:
                continue
            remaining_length = kmer_length
            current_path = path
            if remaining_length > edge.get_length(len(tree.string)):
                if edge.child_node is not None:
                    remaining_length -= edge.get_length(len(tree.string))
                    current_path += tree.string[edge.start : edge.end+1]
                    self._run(tree, edge.child_node, remaining_length, current_path)
                else:
                    continue
            else:
                if tree.string[edge.start+remaining_length-1] == tree.symbol:
                    continue
                current_path += tree.string[edge.start : edge.start+remaining_length]
                if edge.child_node is None:
                    count = 1
                else:
                    count = tree.count_leaves(edge.child_node)
                self.patterns[current_path] = count