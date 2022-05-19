"""Ukkonen Suffix Tree for motif discovery basen on genome-wide evolutionary signature."""

from typing import Tuple, Optional

class Edge:
    """Edge of a Suffix Tree node"""
    def __init__(self, start: int):
        self.start = start
        self.end = None
        self.child_node = None

    def __bool__(self):
        return True

    def get_length(self, current_step: int) -> int:
        """
        Returns edge length, including for open edges.

        :param current_step: current step of the Suffix Tree build (Ukkonen algorithm)
        """
        if self.end is None:
            return current_step  - self.start
        return self.end - self.start + 1

    def split_edge(self, split_index: int, start_index: int) -> 'Node':
        """
        Splits edge, adding a child node with two edges (a new one and the second half of the edge that was split) to 
        the first half of the split edge, and returns the new node.
    
        :param split_index: edge index for split (0 is the first character of the edge)
        :param start_index: string index marking the start of the new edge
        """
        # save end and child_node of the whole edge
        whole_edge_end = self.end
        whole_edge_child_node = self.child_node
        
        # set the first half of split edge
        self.end = self.start + split_index
        self.child_node = Node()

        # set the second half of the split edge and add it to the child node of the first half
        second_split_edge = Edge(self.start + split_index + 1)
        second_split_edge.end = whole_edge_end
        second_split_edge.child_node = whole_edge_child_node
        self.child_node.add_edge(second_split_edge)

        # add new edge to the child node of the first half of the split edge
        new_edge = Edge(start_index)
        self.child_node.add_edge(new_edge)

        return self.child_node

class Node:
    """Suffix Tree node"""
    def __init__(self):
        self.edges = []
        self.suffix_link = None

    def add_edge(self, edge: Edge):
        self.edges += [edge]

class SuffixTree:
    """ 
    Generalized Suffix Tree built with to Ukkonen's algorithm. 
    
    :param string: text input with strings to be parsed. 
    :param separation_symbol: character that separates strings in the text input.
    """
    def __init__(self, string: str, separation_symbol: str):
        self.root = Node()
        self.string = string
        self.symbol = separation_symbol
        if self.string[-1] != self.symbol:
            raise ValueError("Input string must end with the separation symbol. Please check inputs.")
        if self.string.count(self.symbol) > 1:
            self.generalized = True
        else:
            self.generalized = False
        self._build()

    def _match_edge(self, node: Node, char: str) -> Edge:
        """Returns edge from input node that begins with char."""
        for edge in node.edges:
            if self.string[edge.start] == char:
                return edge
        raise Exception("Edge not found")
    
    def _lookup_edge(self, char) -> Optional[Edge]:
        """"Checks if an implicit edge already exists at the active point of the Suffix Tree."""
        if self.active_length == 0:
            try:
                return self._match_edge(self.active_node, char)
            except Exception:
                return None
        else:
            if self._get_active_point_next_char() == char:
                return self.active_edge
            return None

    def _get_active_point_next_char(self) -> str:
        """Returns the character in the string after the active point."""
        return self.string[self.active_edge.start + self.active_length]
    
    def _insert_suffix(self) -> Optional[Node]:
        """
        Inserts current suffix (new edge) after the active point of the tree. 
        If insertion is not made from root, returns node from which insertion was made (condition for suffix link).
        """
        if self.active_length == 0:  # insert straight at active node
            new_edge = Edge(self.step - 1)
            self.active_node.add_edge(new_edge)
            if self.active_node == self.root:
                return None
            return self.active_node
        else:
            new_node = self.active_edge.split_edge(self.active_length - 1, self.step -1)
            return new_node

    def _update_active_point_no_insert(self, existing_edge: Edge):
        """Active point update rule when no insertion is made (suffix is already in the tree)."""
        self.remainder += 1

        if self.active_edge == None or self.active_length == 0: # make sure existing_edge is active_edge
            self.active_edge = existing_edge

        self.active_length += 1

        # update active point if it is at the end of an edge
        self._check_and_canonize(self.active_edge)

    def _update_active_point_from_root(self):
        """Active point update rule when insertion is made from root."""
        self.remainder -= 1
        if self.active_length != 0:
            self.active_length -= 1
        if self.active_length != 0:
            self.active_edge = self._match_edge(self.active_node, self.string[self.step - self.remainder])
            self._check_and_canonize(self.active_edge) # canonize suffix if needed
        else:
            self.active_edge = None
            
    def _update_active_point_from_child(self):
        """Active point update rule when insertion is made from a node other than root."""
        self.remainder -= 1

        if self.active_node.suffix_link is not None:
            self.active_node = self.active_node.suffix_link
        else:
            self.active_node = self.root

        if self.active_edge is not None:
            model_edge = self.active_edge
            self.active_edge = self._match_edge(self.active_node, self.string[model_edge.start])
            self._check_and_canonize(model_edge) # canonize suffix if needed

    def _check_and_canonize(self, model_edge: Edge):
        """
        Checks if the active point overflows or is at the end of a non-leaf edge and update active point if so.
        This is equivalent to Ukkonen's canonize function.
        """
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
        """Core tree construction method"""
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
                if self.generalized == False:
                    no_insert_condition = existing_edge
                else:
                    no_insert_condition = (existing_edge and self.string[self.step-1] != self.symbol)
                if no_insert_condition:
                    # do nothing, add suffix link if needed, update active point (no insert), and move to next step
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

    def _count_leaves(self, node: Optional[Node] = None) -> int:
        """Counts number of leaf nodes below input node"""
        if node is None: 
            node = self.root
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
        """
        Counts the number of occurences of a substring in the Suffix Tree.
        
        :param substring: substring to query.
        """
        substring_edge = self._find_substring(substring)
        if substring_edge is None:
            return 0
        
        if substring_edge.child_node is None:
            return 1
        else:
            return self._count_leaves(substring_edge.child_node)

if __name__ == "__main__":
    a = SuffixTree("AAATGGCCGCGCCG#AAATGGCCGCGCCG#GGCTGTTGAGCGCGCGGGA#", "#")

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