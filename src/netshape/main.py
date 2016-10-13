# Non-Default Imports
import networkx as nx
import community
from networkx.readwrite import json_graph
import numpy as np
import pystache

# Default Imports
import csv
import json
import shutil
import os

class Netshape(object):
    """docstring for Netshape"""
    def __init__(self, dat, sep=","):
        super(Netshape, self).__init__()
        # Maybe you can input source and target
        self.datPath = dat
        with open(dat,'r') as f:
            reader = csv.reader(f, delimiter=sep)
            reader = list(reader)
            try:
                source,target = [list(map(lambda x : x.lower(), reader[0])).index(i) for i in ['source','target']]
                header = reader.pop(0)
                otherVals = [header.index(i) for i in header if i.lower() not in ['source','target']]
                otherHeads= [i for i in header if i.lower() not in ['source','target']]
            except ValueError:
                source = 0
                target = 1

            edges = [dict([('source',str(i[source])),
                 ('target',str(i[target]))] +
                 list(zip(otherHeads, [i[j] for j in otherVals]))) for i in reader]
            nodes = np.unique([(i[source],i[target]) for i in reader])
            nodes = [{'id':i} for i in nodes]
            self.JSONgraph = {'nodes': nodes, 'links':edges}
            self.nodeProps = []
            self.edgeProps = otherHeads
            self.generate_graph().add_eigenvector_centrality().add_community().add_degree()
            self.build_visualization()

    def generate_graph(self,dir=True):
        if dir:
            cu = nx.DiGraph()
        else:
            cu = None
        nx.parse_edgelist([i["source"] + "," + i["target"] for i in self.JSONgraph["links"]], delimiter=",", nodetype=str, create_using=cu)
        self.g = cu
        return self

    def build_visualization(self,title="Network"):
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            pass
        os.makedirs("./dist/data")
        datapath = os.path.splitext(os.path.basename(self.datPath))[0] + ".json"
        self._build('index.html', {
            'netTitle': title,
            'nodeAttrs':[{'attr' : i} for i in self.nodeProps]
        })
        self._build('index.js', {'datapath': datapath})

        with open("./dist/data/" + datapath, 'w') as f:
            json.dump(self.JSONgraph, f)



    def _build(self, path, mapping):
        with open('./tpl/' + path, 'r') as sourceFile:
            tpl = sourceFile.read()
            out = pystache.render(tpl, mapping)
        with open('./dist/' + path,'w') as distFile:
            distFile.write(out)


    def _add_prop(self, prop, propMap):
        # parameter for writing to file
        self.nodeProps.append(prop)
        for i in range(len(self.JSONgraph["nodes"])):
            self.JSONgraph["nodes"][i][prop] = propMap[self.JSONgraph["nodes"][i]["id"]]


    def add_eigenvector_centrality(self):
        centrality = nx.eigenvector_centrality(self.g)
        self._add_prop('Eigenvalue Centrality', centrality)
        return self

    def add_community(self):
        comms = community.best_partition(nx.Graph(self.g))
        self._add_prop('Community', comms)
        return self

    def add_degree(self):
        try:
            in_degree = dict(self.g.in_degree_iter())
            self._add_prop('In Degree', in_degree)
            out_degree = dict(self.g.out_degree_iter())
            self._add_prop('Out Degree', out_degree)
        except nx.NetworkXException:
            pass
        degree = dict(self.g.degree_iter())
        self._add_prop('Degree', degree)
        return self



if __name__ == '__main__':
    a = Netshape('../../../../Data/Nematode/WormNet.csv')

