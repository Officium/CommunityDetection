# -*- coding: utf-8 -*-
import networkx as nx


def load_graph(f, delimiter, skip_rows=0):
    g = nx.Graph()
    with open(f) as fo:
        lines = fo.readlines()[skip_rows:]
    for line in lines:
        try:
            nodex, nodey, weight = line.rstrip("\n").split(delimiter)
        except ValueError:
            continue
        g.add_edge(nodex, nodey, weight=float(weight))

    return g


def removing_based_on_betweeness(g):
    init_ncomp = nx.number_connected_components(g)
    curr_ncomp = init_ncomp
    while curr_ncomp <= init_ncomp:
        bws = nx.edge_betweenness_centrality(g, weight='weight')
        max_bw = max(bws.values())
        # Remove all of the edge with the highest centrality
        for nodes, bw in bws.iteritems():
            if bw == max_bw:
                g.remove_edge(*nodes)
        curr_ncomp = nx.number_connected_components(g)


def get_deg(g):
    adj = nx.adj_matrix(g)
    nodes = g.nodes()
    t = adj.sum(axis=1)
    return {node: t[i, 0] for i, node in enumerate(nodes)}


def get_modularity(g, init_deg, m):
    deg = get_deg(g)
    modularity = 0
    for comp in nx.connected_components(g):
        for node in comp:
            modularity += (deg[node] - init_deg[node] ** 2 / (2 * m))
    return modularity / (2 * m)


def gn(g):
    init_n = g.number_of_edges()
    print "Original graph has {} edges".format(init_n)
    if init_n == 0:
        return None
    m = nx.adj_matrix(g).sum() / 2
    init_deg = get_deg(g)
    i = 1
    while g.number_of_edges():
        removing_based_on_betweeness(g)
        if i % 5 == 0:
            print "iter {} modularity {} number of edges {}"\
                .format(i, get_modularity(g, init_deg, m), g.number_of_edges())
        i += 1
    print "Max modularity: {}".format(get_modularity(g, init_deg, m))
    return nx.connected_components(g)


if __name__ == "__main__":
    graph = load_graph("graph.txt", ",")
    gn(graph)
