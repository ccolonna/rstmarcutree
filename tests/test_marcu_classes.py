#!/usr/bin/env python

# Author: Christian Colonna

""" Test the produced RST is well formed """

from __future__ import print_function

from rstmarcutree import load_tree

# file path and helper
file_path = "test_sentence_nyt.dis"
file_path_2 = "test_JOINT.dis"

# convert .dis representation into python rstmarcu one
rst_tree = load_tree(file_path)
rst_tree_2 = load_tree(file_path_2)

def iterate_over_tree(rst_tree):
    for node in rst_tree.nodes:
        pass

# TESTS
def test_node_count(rst_tree, node_count):
    print("Running test: test node count")
    try:
        assert(len(rst_tree.nodes) == node_count)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Tree nodes: ", len(rst_tree.nodes), " ", node_count)

def test_get_nodes_by_relation(rst_tree): 
    print("Running test: get node by relation")
    try:
        nodes_by_relation = rst_tree.get_nodes_by_relation("Background")
        assert(nodes_by_relation[0].relation == "Background")
        assert(len(nodes_by_relation) == 1)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Relation node: ", nodes_by_relation[0].relation, " ", "Background")

def test_get_nodes_by_relation_file_2(rst_tree):
    print("Running test: get node by relation")
    try:
        nodes_by_relation = rst_tree.get_nodes_by_relation("joint")
        assert(len(nodes_by_relation) == 7)
        nodes_by_relation_2 = rst_tree.get_nodes_by_relation("purpose")
        assert(len(nodes_by_relation_2) == 3)
        last = rst_tree.get_nodes_by_relation("antithesis")
        assert(len(last) == 1)
        # test get_satellite and text
        assert(last[0].get_nucleus().text == 'Upon arrival at the school , however , it became clear that the children were not accustomed to playing with puppets and that the data collection would be a novel experience for them .')
        print("Test passed")

    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Joint node: ", len(nodes_by_relation), 19)
        print("Purpose node:", len(nodes_by_relation_2), 3)
        print("Antithesis node:", len(last), 1)

def test_get_node_childs(rest_tree):
    print("Running test: get node childs")
    try:
        background_node = rst_tree.get_node(10) # we implicitly test also some simple functions
        background_node_2 = rst_tree.get_node(0)
        assert(background_node.child_pointers == [11, 12])
        assert(background_node.childs[0].index == 11)
        assert(background_node.childs[1].index == 12)
        assert(background_node_2.child_pointers == [1, 8])
        assert(background_node_2.childs[0].index == 1)
        assert(background_node_2.childs[1].index == 8)
        assert(rst_tree.get_node(4).childs == None) # Leaf hasn't child
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("node: ", background_node.index, " has childs ", background_node.childs[0].index, background_node.childs[1].index)
        print("root node: ", background_node_2.index, "has childs ", background_node_2.childs[0].index, background_node_2.childs[1].index)

def test_get_edus(rst_tree):
    print("Running test: get node edus")
    try:
        edus = rst_tree.get_edus()
        for edu in edus:
            edu_indexes = [2,4,6,7,11,12,13,15,16]
            assert(edu.index) in edu_indexes
            edu_indexes.remove(edu.index)
        assert(edus[1].text == 'surrounding the American airstrike')
        assert(edus[3].text == 'traveling with him .')
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        for edu in edus:
            print(edu.index, edu.text)

def test_get_edus_file_2(rst_tree):
    print("Running test: get tree edus")
    try:
        edus = rst_tree.get_edus()
        assert(len(edus) == 48)
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Edus number: ", len(edus), 48)

def test_get_parent(rst_tree):
    print("Running test: get parent")
    try:
        child_node = rst_tree.get_node(9)
        assert(child_node.parent == rst_tree.get_node(8))
        assert(child_node.parent.relation == "same-unit")
        assert(rst_tree.get_node(0).parent == None)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("child_node 9:", child_node.index, "parent_node 8:", child_node.parent.index)

def test_get_nucleus_and_get_satellite(rst_tree):
    print("Running test: get nucleus and get satellite")
    try:
        node = rst_tree.get_node(3)
        node_spanning_multinuclear = rst_tree.get_node(8)
        assert(node.get_nucleus() == rst_tree.get_node(4))
        assert(node.get_satellite() == rst_tree.get_node(5))
        assert(node_spanning_multinuclear.get_nucleus() == [rst_tree.get_node(9), rst_tree.get_node(14)])
        assert(node_spanning_multinuclear.get_satellite() == None)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Node 3) Nucleus:", node.get_nucleus().index, "Satellite:", node.get_satellite().index)

def test_promotion_set(rst_tree):
    print("Running test: test promotion set")
    try:
        root = rst_tree.get_node(0)
        salient_texts = [node.text for node in root.promotion_set]
        antithesis = rst_tree.get_nodes_by_relation("antithesis")[0]
        antithesis_texts = [node.text for node in antithesis.promotion_set]
        assert(len(salient_texts) == 13)
        assert("Significant differences were not observed between all and cardinal numbers or all and some ." in salient_texts)
        assert(len(antithesis_texts) == 2)
        assert("and that the data collection would be a novel experience for them ." in antithesis_texts)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print(antithesis_texts)
        print(len(antithesis_texts), "2")
        print(len(salient_texts), "16")

# RUN TESTS

print(" * RUNNING TESTS *")
# Test tree
print("------------------------------")
print("file 1")
print("========================================")
test_node_count(rst_tree, 17)
print("========================================")
test_get_nodes_by_relation(rst_tree)
print("========================================")
# Test node
test_get_node_childs(rst_tree)
print("========================================")
test_get_edus(rst_tree)
print("========================================")
test_get_parent(rst_tree)
print("========================================")
test_get_nucleus_and_get_satellite(rst_tree)
print("========================================")
print("-------------------------------")
print("file 2")
print("========================================")
test_node_count(rst_tree_2, 89)
print("========================================")
test_get_edus_file_2(rst_tree_2)
print("========================================")
test_get_nodes_by_relation_file_2(rst_tree_2)
print("========================================")
test_promotion_set(rst_tree_2)
print("")
print("All test passed!")
