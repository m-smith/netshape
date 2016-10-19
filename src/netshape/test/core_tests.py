import unittest
import os
import sys

from ..main import Netshape
from ..config import conf, Config


PATH = os.path.abspath(__file__)
DIR_PREFIX = os.path.dirname(PATH)

DATA = ['/data/dat_full.csv', '/data/dat_h1.csv', '/data/dat_nh2.csv']
DATA = [DIR_PREFIX + i for i in DATA]

class CoreTests(unittest.TestCase):
    def test_load_from_csv(self):
        ns = Netshape()
        with open(DATA[0], 'r') as f:
            ns.from_edgelist(f)
            self.assertEqual(len(ns.json_graph['links']),7)
            self.assertEqual(sorted([i["id"] for i in ns.json_graph['nodes']]),["1","2","3","4","6"])
            self.assertEqual(set(ns.edge_props),set(['Type','Weight']))
        ns2 = Netshape()
        with open(DATA[1], 'r') as f:
            ns2.from_edgelist(f)
        with open(DATA[2], 'r') as f:
            ns2.from_edgelist(f)
        self.assertEqual(len(ns2.json_graph['links']),7)
        self.assertEqual(sorted([i["id"] for i in ns2.json_graph['nodes']]),["1","2","3","4","6"])
        self.assertEqual(set(ns2.edge_props),set(['Weight','Type']))

    def test_config(self):
        self.assertTrue('build' in conf.commands)
        self.assertEqual(len(conf.commands['build'].pipeline), 4)

    def test_register_and_pipeline_command(self):
        c = Config()
        p = c.register_command('test')
        self.assertTrue('test' in c.commands)
        p.read_edges('network')
        self.assertEqual(len(p.pipeline), 1)
        p.add_node_prop('Eigenvector Centrality', lambda x: x)
        self.assertEqual(len(p.pipeline), 2)


if __name__ == '__main__':
    unittest.main()