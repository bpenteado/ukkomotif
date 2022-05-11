"""
Ukkonen Suffix Tree for motif discovery basen on genome-wide evolutionary signature.
"""

class Edge:
    """ Edge of a Suffix Tree node """
    def __init__(self, data: list):
        self.data = data
        self.child_node = None

    def __bool__(self):
        return True

    def get_length(self):
        return self.data[-1] - self.data[0]

class Node:
    """ Suffix Tree node """
    def __init__(self):
        self.edges = []
        self.suffix_link = None

class SuffixTree:
    """ Suffix Tree """
    def __init__(self):
        self.root = Node()

    def _match_edge(self, char):
        """ Returns edge from active node that begins with char"""
        for edge in self.active_node.edges:
            if self.string[edge.data[0]] == char:
                    return edge
        raise Exception("Edge not found")
    
    def _lookup_edge(self, char):
        """" Checks if implicit edge already exists at active_point in the Suffix Tree """
        if self.active_length == 0:
            try:
                return self._match_edge(char)
            except Exception:
                return None
        else:
            if self._get_active_point_char() == char:
                return self.active_edge
            return None

    def _get_active_point_char(self):
        return self.string[self.active_edge.data[self.active_length]]
    
    def _insert_node(self):
        pass

    def _update_active_point_no_insert(self, existing_edge: Edge):
        self.remainder += 1
        
        # make sure existing_edge is active_edge
        if self.active_edge == None or self.active_length == 0:
            self.active_edge = existing_edge

        self.active_length += 1

        # update active point if it is at the end of an edge
        if self.active_edge.get_length() == self.active_length:
            self.active_node = self.active_edge.child_node
            self.active_edge = None
            self.active_length = 0

    def _update_active_point_from_root(self):
        self.remainder -= 1

        if self.active_length != 0:
            self.active_length -= 1
        
        self.active_edge = self._match_edge(self.string[self.step - self.remainder])
    
    def _update_active_point_from_child(self):
        self.remainder -= 1

        if self.active_node.suffix_link is not None:
            self.active_node = self.active_node.suffix_link
        else:
            self.active_node = self.root

    def build(self, string: str):
        self.string = string
        self.step = 1
        self.active_node = self.root
        self.active_length =  0
        self.active_edge = None
        self.remainder = 1

        while(self.step <= len(self.string)):
            if(self.remainder == 0): 
                self.remainder = 1
            previous_inserted_node = None
            while (self.remainder != 0):
                existing_edge = self._lookup_edge(self.string(self.step-1))
                if existing_edge:
                    self._update_active_point_no_insert(existing_edge)
                    self.step += 1
                    break
                else:
                    # insert new node
                    new_node = self._insert_node()

                    # update active point
                    if self.active_node == self.root:
                        self._update_active_point_from_root()
                    else:
                        self._update_active_point_from_child()

                    # add suffix link if new node is not the first to be added in the current step
                    if previous_inserted_node is not None:
                        previous_inserted_node.suffix_link = new_node
                    previous_inserted_node = new_node

                    if self.remainder == 0:
                        self.step += 1




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