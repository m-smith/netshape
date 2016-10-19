"""The main netshape module which contains the Netshape graph representation
class"""
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
    """ The netshape class. Netshape objects maintain the network state through
        two primary attributes:

        :code:`self.json_graph`
            The JSON representation of the graph, which maintains nodes and
            links as lists of dicts. This is what is eventually written to the
            data file used for the web UI.

             :code:`self.json_graph = {'nodes': [], 'links':[]}`

        :code:`self.g`
            a networkx representation of the network. This is useful for computation
            of network statistics.

    """
    def __init__(self):
        super(Netshape, self).__init__()
        self.json_graph = {'nodes': [], 'links':[]}
        self.node_props = []
        self.edge_props = []
        self.g = nx.Graph()

    def from_edgelist(self, edgelist, sep=",", directed=True):
        """Reads a csv formatted edgelist and adds nodes and edges to the
           network accordingly. If there is a header, the columns labeled 'source',
           and 'target' will be used as node ID's, and any other columns, edge attributes.
           Otherwise, the first two columns will be used as node ID's.

           *Positional arguments:*
                .. option:: edgelist

                    the file to be opened

           *Keyword arguments:*

                .. option:: sep

                    the delimiter string in the csv (default: " , ")

                .. option:: directed

                    boolean indicating true if the graph is directed (default: True)
        """
        try:
            reader = csv.reader(edgelist, delimiter=sep)
            reader = list(reader)
            other_vals = []
            other_heads = []
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
            old_nodes = [i["id"] for i in self.json_graph["nodes"]]
            nodes = [{'id':i} for i in nodes if i not in old_nodes]
            self.json_graph = {
                'nodes': self.json_graph['nodes'] + nodes,
                'links': self.json_graph['links'] + edges}
            self.node_props = self.node_props
            self.edge_props = list(np.unique(self.edge_props + other_heads))
            self._generate_graph(directed)
        finally:
            edgelist.close()

    def _generate_graph(self, directed=True):
        """Builds a networkx graph from the existing json_graph"""

        if directed:
            graph = nx.DiGraph()
        else:
            graph = None
        nx.parse_edgelist([i["source"] + "," + i["target"] for i in self.json_graph["links"]],
                          delimiter=",", nodetype=str, create_using=graph)
        self.g = graph
        return self

    def _write_node_props(self, proplist, sep=",", file=False, header=True):
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

    def build_visualization(self, out="dist", title="Network"):
        """Scaffolds the visualization project into a directory named dist"""
        try:
            FileNotFoundError
        except NameError:
            FileNotFoundError = OSError

        try:
            shutil.rmtree(out)
        except OSError:
            pass
        os.makedirs("./"+ out +"/data")
        datapath = "data" + ".json"
        _build('index.html', {
            'netTitle': title,
            'nodeAttrs':[{'attr' : i} for i in self.node_props]
        })
        _build('index.js', {'datapath': datapath})

        with open("./"+ out +"/data/" + datapath, 'w') as f:
            json.dump(self.json_graph, f)

    def add_node_prop(self, prop, prop_map):
        """Adds a node property to the json_graph
        *Positional arguments:*
            .. option:: prop

                The name of the property to add

            .. option:: prop_map

                A mapping from node ID's to property values


        """
        self.node_props.append(prop)
        for i in range(len(self.json_graph["nodes"])):
            self.json_graph["nodes"][i][prop] = prop_map[self.json_graph["nodes"][i]["id"]]

def _build(path, mapping):
    with open(DIR_PREFIX + '/tpl/' + path, 'r') as source_file:
        tpl = source_file.read()
        out = pystache.render(tpl, mapping)
    with open('./dist/' + path, 'w') as dist_file:
        dist_file.write(out)
