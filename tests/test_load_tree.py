#!/usr/bin/env python

# Author: Christian Colonna

""" Test the tree is correctly loaded """

from __future__ import print_function

from rstmarcutree import load_tree


# file path and helper
file_path = "test_short_sentence.dis"

print(" * RUNNING TESTS *")
# Test tree
print("------------------------------")
print("Tree loading test")
print("========================================")
rst_tree = load_tree(file_path)
print("Test passed, tree correctly load")
print("========================================")
