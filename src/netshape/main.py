"""The main netshape module"""
import csv
import json
import shutil
import os
import sys

import networkx as nx
import community
import numpy as np
import pystache

PATH = os.path.abspath(__file__)
DIR_PREFIX = os.path.dirname(PATH)

class Netshape(object):
    """docstring for Netshape"""
    def __init__(self, path, sep=","):
        super(Netshape, self).__init__()
        # Maybe you can input source and target
        try:
            reader = csv.reader(path, delimiter=sep)
            reader = list(reader)
            try:
                source, target = [list(map(lambda x: x.lower(), reader[0])).index(i)
                                  for i in ['source', 'target']]
                header = reader.pop(0)
                other_vals = [header.index(i) for i in header
                              if i.lower() not in ['source', 'target']]
                other_heads = [i for i in header if i.lower() not in ['source', 'target']]
            except ValueError:
                source = 0
                target = 1

            edges = [dict([('source', str(i[source])), ('target', str(i[target]))]
                          + list(zip(other_heads, [i[j] for j in other_vals]))) for i in reader]
            nodes = np.unique([(i[source], i[target]) for i in reader])
            nodes = [{'id':i} for i in nodes]
            self.json_graph = {'nodes': nodes, 'links':edges}
            self.node_props = []
            self.edge_props = other_heads
            self.g = None
        finally:
            path.close()

    def generate_graph(self, directed=True):
        """Builds a networkx graph from the provided edgelies"""
        if directed:
            graph = nx.DiGraph()
        else:
            graph = None
        nx.parse_edgelist([i["source"] + "," + i["target"] for i in self.json_graph["links"]],
                          delimiter=",", nodetype=str, create_using=graph)
        self.g = graph
        return self

    def write_node_props(self, proplist, sep=",", file=False, header=True):
        """Writes csv formatted node property list
        Positional arguments:
        proplist -- the list of attribute names to write

        Keyword arguments:
        sep    -- the separator string between csv values (default ",")
        file   -- the file to write to, or False for stdout (default False)
        header -- true if a header row should be output, false otherwise
        """
        try:
            f = open(file, 'w') if file else sys.stdout
            if header:
                f.write(sep.join([str(i) for i in proplist]) + "\n")
            for node in self.json_graph["nodes"]:
                f.write(sep.join([str(node[i]) for i in proplist]) + "\n")
        finally:
            if f is not sys.stdout:
                f.close()

    def build_visualization(self, title="Network"):
        """Scaffolds the visualization project into a directory named dist"""
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            pass
        os.makedirs("./dist/data")
        datapath = "data" + ".json"
        _build('index.html', {
            'netTitle': title,
            'nodeAttrs':[{'attr' : i} for i in self.node_props]
        })
        _build('index.js', {'datapath': datapath})

        with open("./dist/data/" + datapath, 'w') as f:
            json.dump(self.json_graph, f)

    def add_node_prop(self, prop, prop_map):
        """Adds a node property to the json_graph

        Positional arguments:
        prop     -- the name of the property to add
        prop_map -- a map from nodes to the property being added
        """
        self.node_props.append(prop)
        for i in range(len(self.json_graph["nodes"])):
            self.json_graph["nodes"][i][prop] = prop_map[self.json_graph["nodes"][i]["id"]]


    def add_eigenvector_centrality(self):
        """Hardcoded centrality"""
        centrality = nx.eigenvector_centrality(self.g)
        self.add_node_prop('Eigenvalue Centrality', centrality)
        return self

    def add_community(self):
        """Hardcoded community detection"""
        comms = community.best_partition(nx.Graph(self.g))
        self.add_node_prop('Community', comms)
        return self

    def add_degree(self):
        """Hardcoded degree"""
        try:
            in_degree = dict(self.g.in_degree_iter())
            self.add_node_prop('In Degree', in_degree)
            out_degree = dict(self.g.out_degree_iter())
            self.add_node_prop('Out Degree', out_degree)
        except nx.NetworkXException:
            pass
        degree = dict(self.g.degree_iter())
        self.add_node_prop('Degree', degree)
        return self

def _build(path, mapping):
    with open(DIR_PREFIX + '/tpl/' + path, 'r') as source_file:
        tpl = source_file.read()
        out = pystache.render(tpl, mapping)
    with open('./dist/' + path, 'w') as dist_file:
        dist_file.write(out)
