import networkx as nx
import community


def eigenvector_centrality(ns, name, _):
    """Computes eigenvector centrality for all nodes"""
    centrality = nx.eigenvector_centrality(ns.g)
    ns.add_node_prop(name, centrality)
    return centrality

def modularity_community(ns, name, _):
    """Community detection"""
    comms = community.best_partition(nx.Graph(ns.g))
    ns.add_node_prop(name, comms)
    return comms

def degree(ns, name, _):
    degree = dict(ns.g.degree_iter())
    ns.add_node_prop(name, degree)
    return degree

def in_degree(ns, name, _):
    try:
        in_degree = dict(ns.g.in_degree_iter())
        ns.add_node_prop(name, in_degree)
    except nx.NetworkXException as err:
        print("Cannot compute in-degree of undirected graph")
        raise err
    return in_degree

def out_degree(ns, name, _):
    try:
        out_degree = dict(ns.g.out_degree_iter())
        ns.add_node_prop('Out Degree', out_degree)
    except nx.NetworkXException as err:
        print("Cannot compute out-degree of undirected graph")
        raise err
    return out_degree
