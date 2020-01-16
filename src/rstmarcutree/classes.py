#!python

""" classes.py: classes for RST Marcu tree generation: RSTTree and RSTNode """

__author__ = "Christian Colonna"

from Queue import Queue

from discoursegraphs import read_distree


class RSTNode(object):
    """ Marcu RST tree node """
    def __init__(self, index, status, relation, schema, parent_pointer, child_pointers, text, parent, childs, promotion_set):
        self.index = index
        self.status = status # ROOT, NUCLEUS or SATELLITE
        self.relation = relation # Relations or LEAF
        self.schema = schema # MULTINUCLEAR or DEPENDENT
        self.parent_pointer = parent_pointer # parent
        self.child_pointers = child_pointers # list of childs
        self.text = text # the text spanned by the node
        self.parent = parent
        self.childs = childs
        self.promotion_set = promotion_set # the promotion or saliency set
    
    def get_nucleus(self):
        """ It returns the nucleus of the node,
            a list of nucleus if the node surrounds a multinuclear relation.
            None if the node is an edu.
        """
        if self.schema == 'MULTINUC':
            return self.childs
        elif self.relation == 'LEAF':
            return None
        else:
            for child in self.childs:
                if child.status == 'N':
                    return child 

    def get_satellite(self):
        """ It returns the satellite of a node:
            None if the node surrounds a multinuclear relation.
            None if the node is an edu.
        """
        for child in self.childs:
            if child.status == 'S':
                return child
        return None

class RSTTree(object):
    """
    A class that represents a Marcu RST tree as it is described in paper:
    Building Up Rhetorical Structure Trees 1996.
    This is composed by RSTNode.
    Root has pointer 0.

    RSTTree is composed by RSTNode
    """
    def __init__(self, nodes):
        def rescale_tree_to_set_parent_and_childs_and_promotion_sets(nodes):
            """ parent and childs are set by pointers
            """
            def get_node_by_index(index, nodes):
                for node in nodes:
                    if node.index == index:
                        return node
        
            def get_most_important_units(node):
                """ Function use queue, scanning nodes, if the might be important they are added to the queue.
                    Then one at a time are examined to see if are important.
                    They are important relative to a node if are nucleus of the node and terminal.
                """
                def is_important(node):
                    return not node.get_nucleus()

                queue = Queue()
                queue.put(node)

                while not queue.empty():
                    possible_important_node = queue.get()
                    if is_important(possible_important_node):
                        node.promotion_set.append(possible_important_node) # if important add to promotion set
                    if possible_important_node.childs:
                        # the might be important if nucleus, add them to the queue!    
                        other_possible_important_nodes = [child for child in possible_important_node.childs if child.status == 'N']
                        for other_possible_important_node in other_possible_important_nodes:
                            queue.put(other_possible_important_node)

            # childs and parents                 
            for node in nodes:
                if node.parent_pointer is not None:
                    node.parent = get_node_by_index(node.parent_pointer, nodes)
                if node.child_pointers:
                    node.childs = [get_node_by_index(child_pointer, nodes) for child_pointer in node.child_pointers]
        
            # promotion sets
            for node in nodes:    
                get_most_important_units(node)

        rescale_tree_to_set_parent_and_childs_and_promotion_sets(nodes)
        self.nodes = nodes
    
    def get_nodes_by_relation(self, relation):
        """ Return a list of tree nodes by relation they span
        """
        nodes_by_relation = []
        for node in self.nodes:
            if node.relation == relation:
                nodes_by_relation.append(node)
        return nodes_by_relation

    def get_edus(self):
        """ Return edu's of the tree
        """
        return self.get_nodes_by_relation("LEAF")

    def get_node(self, index):
        """ Return the node by index
        """
        for node in self.nodes:
            if node.index == index:
                return node 


class RSTEDUAligner(object):
    """ This object helps to align the edu text (elementary discourse unit) of RSTTree to the original
        plain text consumed by the rst parser. This may be necessary since the parser tokenize the text
        inserting spaces and causing disalignment.    
    """
    @staticmethod
    def get_original_edu_offsets(edus, original_text):
        """ Return the boundaries of an edu in original plain text. We process all the file in a hit.
            This way we always know the initial boundary of the edu since it starts from zero.     
        """
        edu_offsets = [] # ((starts_char, end_char), index)
        new_edus = []
        starts_at = 0 # the position where the current edu starts 

        for old_edu in edus:
            
            last_edu_token = old_edu.text.split()[-1]  # the terminal token of the edu

            # all the candidates that can be the end of the edu
            edu_ending_boundary_candidates = [(i + len(last_edu_token)) for i in RSTEDUAligner.find_all_occurences(last_edu_token, original_text[starts_at:])]
            
            # we select the candidate such as the length last_char  - starts_at is the closest to
            # len(tokenized edu)
            
            winning_candidate = 0
            for possible_terminal_char in edu_ending_boundary_candidates:
                if abs((len(old_edu.text)) - possible_terminal_char) <= abs((len(old_edu.text)) - winning_candidate):
                    winning_candidate = possible_terminal_char
                ends_at = winning_candidate + starts_at
            
            edu_offsets.append(((starts_at, ends_at),old_edu.index))
            new_edus.append(original_text[starts_at:ends_at])

            try:
                for token in old_edu.text.split():
                    assert(token in original_text[starts_at:ends_at])
            except:
                print("There's a bug, edu not aligned")
                print(" TODO") 
                # TODO: if there are more tokens, check first if it belongs to the previous edu if not it
                # belongs to next one. Adjust boundaries! Big mess! 
                # Recursion? While?
                exit

            # move the pointer: this makes the search of ending token (n log n) to the length of the document
            starts_at = ends_at
        try:
            assert(original_text == ''.join(new_edus))           
        except:
            print("There's a bug, length of plain text != text derived by concatenation of new edu")
            print("To correct this you need TODO: ")
            print(" while if ")
            print("CONCATENATED EDUS TEXT")
            print(''.join(new_edus))
            print(len(''.join(new_edus)))
            print(original_text)
            print("ORIGINAL TEXT")
            print(len(original_text))
            exit           
        return(edu_offsets)

    @staticmethod
    def read_plain_text(plain_text_path):
        with open(plain_text_path) as fh:
            lines = []
            for line in fh:
                lines.append(line)
            return ''.join(lines)[0:-1] # we remove a final /n
    @staticmethod
    def find_all_occurences(p, s):
        """ Yields all the occurences of the substring p in the string s.
        """
        i = s.find(p)
        while i != -1:
            yield i
            i = s.find(p, i+1)


class RSTTreeHelper(object):
    """ A class that scan and analyze a DGParentedTree representation of an RST tree.
        This class is necessary while the nltk representation used by discoursegraphs
        is hard to handle. 
        The main problem is RST tr 
        ==>   Since the helper want to scan nodes i will use 'node' as name for 'subtree'.

        The helper produce a RSTTree representation of the discourse tree by composition of RSTNode  
    """
    ROOT = 'ROOT'
    NUCLEUS = 'N'
    SATELLITE = 'S'
    MULTINUCLEAR = 'MULTINUC'
    DEPENDENT = 'DEP'
    LEAF = 'LEAF'

    def parse_tree_nodes(self, dis_tree_file_path, filter_function=None):
        
        tree = self.load_dis_tree(dis_tree_file_path)
        marcu_rst_nodes = [] # this nodes will be used to generate a RSTTree

        self.inject_unique_id(tree) # injecting pointers 
        
        for node in tree.subtrees():
            if node.idx == 'DUP': # Don't parse duplicate
                continue
            if self.node_is_tree_root(node):
                index = node.idx
                status = self.ROOT
                relation = node.label()
                schema = self.get_node_schema(node)
                parent_pointer = None
                child_pointers = self.get_child_indexes(node)
                text = self.get_node_spanned_text(node)        
            # parse the leaves
            elif self.node_is_leaf(node): 
                index = node.idx
                status = node.label()
                relation = self.LEAF
                schema = None
                parent_pointer = node.parent().parent().idx  # TODO debug ATTENTION maybe error
                child_pointers = None
                text = self.get_node_spanned_text(node)
            # parse intermidiate node, Nucleus, Satellite, beaware to Arc Relation
            elif self.node_is_satellite_or_nucleus(node): 
                index = node.idx
                status = node.label()
                relation = node[0].label()
                schema = self.get_node_schema(node[0])
                parent_pointer = self.evaluate_middle_node_parent_index(node)
                child_pointers = self.get_child_indexes(node[0])
                text = self.get_node_spanned_text(node)               
            
            rst_node = RSTNode(index, status, relation, schema, parent_pointer, child_pointers, text, None, None, [])
            marcu_rst_nodes.append(rst_node)

        return RSTTree(marcu_rst_nodes)

    def inject_unique_id(self, tree):
        """ As nltk tree unary_collapse doesn't work we recreate the tree data 
            structure as a directed acyclyc dependency graph, we inject unique id
            and set DUP label to node being instead relation_arc_label
            Example:
                
                    |
                    N idx: 2
                    |
                BACKGROUND idx: DUP
                 /   \\
        idx:3  S       N  idx:4    
        """        
        i = 0
        for subtree in tree.subtrees():
            if self.node_is_not_node_but_relation_arc_label(subtree):
                subtree.idx = 'DUP'
            else:
                subtree.idx = i
                i += 1

    def evaluate_middle_node_parent_index(self, node):
        """ Special function: arc_relation_node has index DUP,
            middle node indexes are evaluated ingoring these
        """
        if node.parent().idx != 'DUP':
            return node.parent().idx
        else:
            return node.parent().parent().idx    

    def get_child_indexes(self, node):
        """ As indexes has been injected in a DGParentedTree, 
            function returns child indexes of a node
        """
        return [child.idx for child in node]

    # TODO implement this
    def get_node_status(self, node):
        raise NotImplementedError("To be implemented yet")
    
    def get_node_relation(self, node):
        """ Check which relation exists for a node
        """
        return node.parent().label()

    # TODO DEBUG check the behaviour with DUP node    
    def get_node_schema(self, node):
        """ Check if relation is multinuclear (Joint, Sequence ...)
            or dependent (Condition, Attribution ...)
        """
        childs = [child for child in node]
        nucleus_counter = 0
        for child in childs:
            if child.label() in 'N':
                nucleus_counter +=1
        if len(childs) > 2 or nucleus_counter > 1:
            return self.MULTINUCLEAR
        else:
            return self.DEPENDENT
    
    def get_node_spanned_text(self, node):
        """ Return the portion of text spanned by a node. 
            For edu's the text is the edu itself.
        """
        return ' '.join(node.leaves())

    def node_is_tree_root(self, tree_node):
        """ Check if node is root
        """
        return tree_node.parent() is None
    
    def node_is_satellite_or_nucleus(self, node):
        """ Check if the DGParentedTree node is Satellite or Nucleus
        """
        return node.label() in ("S", "N")
    
    def node_is_not_node_but_relation_arc_label(self, node):
        """ DGParentedTree has a problem: relation arc label is treat as a node. 
            We need to clean this as it is useful just for printing the tree.
            All the relations in .dis file except the root relation are treat like this
        """
        if node.parent() is None: # root is special relation
            return False
        else:    
            return node.label() not in ("S", "N")


    def node_is_leaf(self, tree):
        """ Check if a node is leaf in a DGParentedTree
        """ 
        return tree.height() == 2

    def load_dis_tree(self, file_path):
        """ Arg: str : path to the .dis file
            -> DGParentedTree : (A discoursegraphs subclass of nltk ParentedTree) discourse_tree
        """
        return read_distree(file_path).tree
