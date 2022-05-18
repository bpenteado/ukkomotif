"""
Ukkonen Suffix Tree for motif discovery basen on genome-wide evolutionary signature.
"""

from typing import Tuple

class Edge:
    """ Edge of a Suffix Tree node """
    def __init__(self, start: int):
        self.start = start
        self.end = None
        self.child_node = None

    def __bool__(self):
        return True

    def get_length(self, current_step: int):
        if self.end is None:
            return current_step  - self.start
        return self.end - self.start + 1

    def split_edge(self, split_index: int, start_index: int):
        # save current end child_node
        whole_edge_end = self.end
        whole_edge_child_node = self.child_node
        # set end index
        self.end = self.start + split_index
        # set child node
        self.child_node = Node()
        # add split edge to child node
        split_edge = Edge(self.start + split_index + 1)
        split_edge.end = whole_edge_end
        split_edge.child_node = whole_edge_child_node
        self.child_node.add_edge(split_edge)
        # add new edge to child node
        new_edge = Edge(start_index)
        self.child_node.add_edge(new_edge)
        # return newly created node (child node)
        return self.child_node

class Node:
    """ Suffix Tree node """
    def __init__(self):
        self.edges = []
        self.suffix_link = None

    def add_edge(self, edge: Edge):
        self.edges += [edge]

class SuffixTree:
    """ Suffix Tree """
    def __init__(self, string: str, separation_symbol: str):
        self.root = Node()
        self.string = string
        self.symbol = separation_symbol
        self._build()

    def _match_edge(self, node: Node, char: str) -> Edge:
        """ Returns edge from input node that begins with char"""
        for edge in node.edges:
            if self.string[edge.start] == char:
                    return edge
        raise Exception("Edge not found")
    
    def _lookup_edge(self, char):
        """" Checks if an implicit edge already exists at the active point of the Suffix Tree """
        if self.active_length == 0:
            try:
                return self._match_edge(self.active_node, char)
            except Exception:
                return None
        else:
            if self._get_active_point_next_char() == char:
                return self.active_edge
            return None

    def _get_active_point_next_char(self):
        # TODO: handle case where active_edge is null
        return self.string[self.active_edge.start + self.active_length]
    
    def _insert_suffix(self):
        if self.active_length == 0:
            # add edge straight to active node
            new_edge = Edge(self.step - 1)
            self.active_node.add_edge(new_edge)
            if self.active_node == self.root:
                return None
            return self.active_node
        else:
            # split active_edge and return new node
            # TODO: what if the active point is at the "end" of an open edge?
            new_node = self.active_edge.split_edge(self.active_length - 1, self.step -1)
            return new_node

    def _update_active_point_no_insert(self, existing_edge: Edge):
        self.remainder += 1
        
        # make sure existing_edge is active_edge
        if self.active_edge == None or self.active_length == 0:
            self.active_edge = existing_edge

        self.active_length += 1

        # update active point if it is at the end of an edge
        self._check_and_canonize(self.active_edge)

    def _update_active_point_from_root(self):
        self.remainder -= 1

        if self.active_length != 0:
            self.active_length -= 1
        
        #TODO: Shouldnt this be the same as from chil canonization
        if self.remainder != 0 and self.active_length != 0:
            self.active_edge = self._match_edge(self.active_node, self.string[self.step - self.remainder])
        else:
            self.active_edge = None
    
    def _update_active_point_from_child(self):
        self.remainder -= 1

        # update active node
        if self.active_node.suffix_link is not None:
            self.active_node = self.active_node.suffix_link
        else:
            self.active_node = self.root

        # update active edge (canonizing if needed)
        if self.active_edge is not None:
            model_edge = self.active_edge
            self.active_edge = self._match_edge(self.active_node, self.string[model_edge.start])
            self._check_and_canonize(model_edge)

    def _check_and_canonize(self, model_edge: Edge):
        """ Checks if the active point overflows or is at the end of a non-leaf edge and update active point if so (canonize)"""
        remaining_edge_start = model_edge.start
        while self.active_length >= self.active_edge.get_length(self.step):
            limiting_edge_length = self.active_edge.get_length(self.step)    
            if self.active_edge.child_node is not None:
                self.active_node = self.active_edge.child_node
                if self.active_length == limiting_edge_length:
                    self.active_edge = None
                    self.active_length = 0
                    return
                else:
                    remaining_edge_start += limiting_edge_length
                    self.active_edge = self._match_edge(self.active_node, self.string[remaining_edge_start])
                    self.active_length -= limiting_edge_length
            else:
                if self.active_length > limiting_edge_length:
                    raise Exception("Unexpected error: tree overflow")
                return

    def _build(self):
        self.step = 1
        self.active_node = self.root
        self.active_length =  0
        self.active_edge = None
        self.remainder = 1

        while(self.step <= len(self.string)):
            # reset remainder if all suffixes have been added in the previous step
            if(self.remainder == 0): 
                self.remainder = 1
            previous_internal_node = None # resetting for the new step
            while (self.remainder != 0):
                # check if the current suffix is implicitly contained in the tree 
                existing_edge = self._lookup_edge(self.string[self.step-1])
                if existing_edge:
                    # do nothing, update active point (no insert), and move to next step
                    if previous_internal_node is not None:
                        if previous_internal_node.suffix_link is None:
                            previous_internal_node.suffix_link = self.active_node
                    self._update_active_point_no_insert(existing_edge)
                    self.step += 1
                    break
                else:
                    # insert current suffix at active point and return newly created node (None if no node was created)
                    internal_node = self._insert_suffix()

                    # update active point
                    if self.active_node == self.root:
                        self._update_active_point_from_root()  # update rule for edge insert at root node
                    else:
                        self._update_active_point_from_child()  # update rule for edge insert at non-root node

                    # add suffix link if new node is not the first to be added in the current step
                    if internal_node is not None and previous_internal_node is not None:
                        previous_internal_node.suffix_link = internal_node

                    if internal_node is not None:
                        previous_internal_node = internal_node

                    if self.remainder == 0:
                        self.step += 1

    def _count_leaves(self, node: Node) -> int:
        """Counts number of leaf nodes below input node"""
        count = 0
        for edge in node.edges:
            if edge.child_node is None:
                count += 1
            else:
                count += self._count_leaves(edge.child_node)
        return count

    def _find_substring(self, substring: str) -> Tuple[Node, Edge]:
        """Searches for substring and returns its edge if found"""
        current_node = self.root
        try:
            match_edge = self._match_edge(current_node, substring[0])
        except Exception:
            return None
        steps_in_edge = 0
        for i, character in enumerate(substring):
            if self.string[match_edge.start + steps_in_edge] == character:
                steps_in_edge += 1
                if steps_in_edge == match_edge.get_length(len(self.string)):
                    if i == len(substring) - 1:
                        return match_edge
                    else:
                        if match_edge.child_node is None:
                            return None
                        current_node = match_edge.child_node
                        try:
                            match_edge = self._match_edge(current_node, substring[i+1]) 
                        except Exception:
                            return None
                        steps_in_edge = 0
            else:
                return None
        return match_edge

    def count_substring(self, substring: str) -> int:
        """Counts the number of occurences of a substring in the Suffix Tree"""
        substring_edge = self._find_substring(substring)
        if substring_edge is None:
            return 0
        
        if substring_edge.child_node is None:
            return 1
        else:
            return self._count_leaves(substring_edge.child_node)

if __name__ == "__main__":
    a = SuffixTree("AAAATCTACGCGGCGCGCGCTGGGCTA!AAAATCTACGCTTTTCGCGCTGGGCTA?TTTAAAATCTACGCGGCGCGCGCTGG#", "#")
    
########################################################################################
def stringer(input_string: str) -> str:
    """
    Type filter that raises an error for non-string inputs.

    :param input_string: input to be filtered.

    :raises TypeError: if input_string is not a string.
    """
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    return input_string