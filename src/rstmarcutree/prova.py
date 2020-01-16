from rstmarcutree import load_tree
from discoursegraphs import read_distree

tree = load_tree('test_JOINT.dis')

# tree = read_distree('text.dis')

print(tree.get_height())

for node in tree.nodes:
    if node.relation == 'LEAF':
         print node.get_normalized_saliency_score()

