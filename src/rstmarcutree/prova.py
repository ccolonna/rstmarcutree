from rstmarcutree import load_tree
from discoursegraphs import read_distree

tree = load_tree('text.dis')

# tree = read_distree('text.dis')
# for node in tree.tree.subtrees():
#     print node


print("index  status  relation  schema   p_pointer   c_pointers   parent    childs ")

for node in tree.nodes:
    print(node, node.index, node.status, node.relation, node.schema, node.parent_pointer,node.child_pointers,node.parent,node.childs)
    print("")