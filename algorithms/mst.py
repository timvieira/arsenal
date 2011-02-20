from datastructures.unionfind import UnionFind

'''
def mst(G):
    """
    Find the minimum spanning tree (mst) of an undirected graph G.

    `G` should be a symmetric adjacency matrix. The mst is returned
    as a list of edges.
    """

    N = G.shape[0]
    assert G.shape[0] == G.shape[1]
    
    # Kruskal's algorithm: sort edges by weight, and add them one at a time.
    # We use Kruskal's algorithm, first because it is very simple to
    # implement once UnionFind exists, and second, because the only slow
    # part (the sort) is sped up by being built in to Python.
    subtrees = UnionFind()
    tree = []
    edges = [(G[u,v],u,v) for u in xrange(N) for v in xrange(N) if u != v]
    edges.sort()
    for (_,u,v) in edges:
        if subtrees[u] != subtrees[v]:
            tree.append((u,v))
            subtrees.union(u,v)
    return tree        
'''

def mst(G):
    """
    Return the minimum spanning tree of an undirected graph G.
    G should be represented in such a way that G[u][v] gives the
    length of edge u,v, and G[u][v] should always equal G[v][u].
    The tree is returned as a list of edges.
    """
    
    # Kruskal's algorithm: sort edges by weight, and add them one at a time.
    # We use Kruskal's algorithm, first because it is very simple to
    # implement once UnionFind exists, and second, because the only slow
    # part (the sort) is sped up by being built in to Python.
    subtrees = UnionFind()
    tree = []
    edges = [(G[u][v],u,v) for u in G for v in G[u]]
    edges.sort()
    for (_,u,v) in edges:
        if subtrees[u] != subtrees[v]:
            tree.append((u,v))
            subtrees.union(u,v)
    return tree        
