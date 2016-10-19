import unittest
import os

import networkx as nx
import community

from ..main import Netshape
from .. import node_props as n_p

PATH = os.path.abspath(__file__)
DIR_PREFIX = os.path.dirname(PATH)

DATA = '/data/WormNet.csv'
DATA = DIR_PREFIX + DATA

class NodePropsTest(unittest.TestCase):
    def test_eigenvector_centrality(self):
        ns = Netshape()
        with open(DATA, 'r') as f:
            ns.from_edgelist(f)
        true_cent = nx.eigenvector_centrality(ns.g)
        test_cent = n_p.eigenvector_centrality(ns, '', True)
        self.assertAlmostEqual(set(true_cent), set(test_cent))

    def test_community_detection(self):
        ns = Netshape()
        with open(DATA, 'r') as f:
            ns.from_edgelist(f)
        true_comm = community.best_partition(nx.Graph(ns.g))
        test_comm = n_p.modularity_community(ns, '', True)
        self.assertEqual(true_comm, test_comm)

    def test_degree(self):
        ns = Netshape()
        with open(DATA, 'r') as f:
            ns.from_edgelist(f)
        true = dict(ns.g.degree_iter())
        test = n_p.degree(ns, '', True)
        self.assertEqual(true,test)

if __name__ == '__main__':
    unittest.main()