#!python 

""" Function takes as input the path to a .dis file representing a discourse tree and returns """
""" an object oriented representation enriched with Daniel Marcu attributes 1996 1999 """

__author__ = "Christian Colonna"

from classes import RSTTreeHelper

def load_tree(dis_file_path):
    """ Example of usage:

        >>> from rstmarcutree import load_tree
        >>> rst_tree = load_marcu_tree('path_to_rst_file.dis')

        then you can access all the attributes and methods of the tree for example:
        
        to get the root:
        >>> tree_root = rst_tree.get_node(0)

        To return satellite and nucleus of the root:

        >>> tree_root.get_satellite()
        >>> tree_root.get_nucleus()

    """
    rst_helper = RSTTreeHelper()
    return rst_helper.parse_tree_nodes(dis_file_path)
