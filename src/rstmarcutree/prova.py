from rstmarcutree import load_tree
from discoursegraphs import read_distree

tree = load_tree('test_JOINT.dis')

# tree = read_distree('text.dis')

for node in tree.get_nodes_by_relation('LEAF'):
    print node.index