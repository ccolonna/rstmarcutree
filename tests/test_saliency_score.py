#!/usr/bin/env python

# Author: Christian Colonna

""" Test the produced RST is well formed """

from __future__ import print_function

from Queue import Queue

from rstmarcutree import load_tree


# file path and helper
file_path = "test_sentence_nyt.dis"

# convert .dis representation into python rst tree one
rst_tree = load_tree(file_path)

print("... Tree loaded")

# TESTS

def test_tree_height(rst_tree):
    print("Running test: test tree height")
    try:
        assert(rst_tree.get_height() == 5)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Tree height", rst_tree.get_height(), 5)

def test_node_depth(rst_tree):
    print("Running test: test node depth")
    node_1 = rst_tree.get_node(7)
    node_2 = rst_tree.get_node(9)
    node_3 = rst_tree.get_node(13)
    try:
        assert(node_1.get_depth() == 4)
        assert(node_2.get_depth() == 2)
        assert(node_3.get_depth() == 3)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Node ", node_1.index, " depth: ", node_1.get_depth(), 4)
        print("Node ", node_2.index, " depth: ", node_2.get_depth(), 2)    
        print("Node ", node_3.index, " depth: ", node_3.get_depth(), 3)    

def test_node_height(rst_tree):
    print("Running test: test node height")
    node_1 = rst_tree.get_node(6)
    node_2 = rst_tree.get_node(13)
    try:
        assert(node_1.get_height() == 1)
        assert(node_2.get_height() == 1)
        print("Test passed")
    except AssertionError, e:
        print(e)
        raise AssertionError
    finally:
        print("Node ", node_1.index, " height: ", node_1.get_height(), 1)
        print("Node ", node_2.index, " height: ", node_2.get_height(), 1)    


def test_saliency_score(rst_tree):
    print("Running test: test saliency score")
    edus = rst_tree.get_edus()
    scores = Queue()
    for s in [5, 3, 2, 1, 1, 4, 2, 4, 2]:
        scores.put(s)
    try:
        for edu in edus:
            # we insert them following the linear order of text
            score = scores.get()
            saliency_score = edu.get_saliency_score()
            assert(saliency_score == score)
        print("Test passed")
    except AssertionError, e:
        print(e)
        print("Tree node", edu.index, "saliency score: ", saliency_score, " ", score, edu.text)
        raise AssertionError

        

# RUN TESTS

print(" * RUNNING TESTS *")
# Test tree
print("------------------------------")
print("file 1")
print("========================================")
test_tree_height(rst_tree)
print("========================================")
test_node_depth(rst_tree)
print("========================================")
test_node_height(rst_tree)
print("========================================")
test_saliency_score(rst_tree)
print("========================================")
