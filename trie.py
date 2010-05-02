# Natural Language Toolkit: Miscellaneous container classes
#
# Copyright (C) 2001-2010 NLTK Project
# Author: Steven Bird <sb@csse.unimelb.edu.au>
# URL: <http://www.nltk.org/>
# For license information, see LICENSE.TXT



# Trie structure, by James Tauber and Leonardo Maffi (V. 1.2, July 18 2006)
# Extended by Steven Bird

class Trie(object):
    """A Trie is like a dictionary in that it maps keys to
    values. However, because of the way keys are stored, it allows
    look up based on the longest prefix that matches.  Keys must be
    strings.
    """

    def __init__(self, trie=None):
        if trie is None:
            self._root = [None, {}, 0]
        else:
            self._root = trie

    def clear(self):
        self._root = [None, {}, 0]

    def isleaf(self, key):
        """Return True if the key is present and it's a leaf of the
        Trie, False otherwise."""

        curr_node = self._root
        for char in key:
            curr_node_1 = curr_node[1]
            if char in curr_node_1:
                curr_node = curr_node_1[char]
            else:
                return False
        return curr_node[0] is not None

    def find_prefix(self, key):
        """Find as much of the key as one can, by using the longest
        prefix that has a value.  Return (value, remainder) where
        remainder is the rest of the given string."""

        curr_node = self._root
        remainder = key
        for char in key:
            if char in curr_node[1]:
                curr_node = curr_node[1][char]
            else:
                return curr_node[0], remainder
            remainder = remainder[1:]
        return curr_node[0], remainder

    def subtrie(self, key):
        curr_node = self._root
        for char in key:
            curr_node = curr_node[1][char]
        return Trie(trie=curr_node)

    def __len__(self):
        return self._root[2]

    def __eq__(self, other):
        return self._root == other._root

    def __ne__(self, other):
        return not (self == other)

    def __setitem__(self, key, value):
        curr_node = self._root
        for char in key:
            curr_node[2] += 1
            curr_node = curr_node[1].setdefault(char, [None, {}, 0])
        curr_node[0] = value
        curr_node[2] += 1

    def __getitem__(self, key):
        """Return the value for the given key if it is present, raises
        a KeyError if key not found, and return None if it is present
        a key2 that starts with key."""

        curr_node = self._root
        for char in key:
            curr_node = curr_node[1][char]
        return curr_node[0]

    def __contains__(self, key):
        """Return True if the key is present or if it is present a
        key2 string that starts with key."""

        curr_node = self._root
        for char in key:
            curr_node_1 = curr_node[1]
            if char in curr_node_1:
                curr_node = curr_node_1[char]
            else:
                return False
        return True

    def __str__(self):
        return str(self._root)

    def __repr__(self):
        return "Trie(%r)" % self._root

