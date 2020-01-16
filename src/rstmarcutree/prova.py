from rstmarcutree import load_tree
from discoursegraphs import read_distree
from classes import RSTEDUAligner

tree = load_tree('t.dis')

# tree = read_distree('text.dis')
# for node in tree.tree.subtrees():
#     print node



original_text = RSTEDUAligner.read_plain_text('t')
original_offsets = RSTEDUAligner.get_original_edu_offsets(tree.get_edus(), original_text)

for offset in original_offsets:
    print original_text[offset[0][0]:offset[0][1]]
    print offset[0]