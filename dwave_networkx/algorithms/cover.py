from dwave_networkx.algorithms.independent_set import maximum_independent_set
from dwave_networkx.utils import binary_quadratic_model_sampler

__all__ = ['min_vertex_cover', 'is_vertex_cover']


@binary_quadratic_model_sampler(1)
def min_vertex_cover(G, sampler=None, **sampler_args):
    """Returns an approximate minimum vertex cover.

    Defines a QUBO with ground states corresponding to a minimum
    vertex cover and uses the sampler to sample from it.

    A vertex cover is a set of vertices such that each edge of the graph
    is incident with at least one vertex in the set. A minimum vertex cover
    is the vertex cover of smallest size.

    Parameters
    ----------
    G : NetworkX graph
        The graph on which to find a minimum vertex cover.

    sampler
        A binary quadratic model sampler. A sampler is a process that
        samples from low energy states in models defined by an Ising
        equation or a Quadratic Unconstrained Binary Optimization
        Problem (QUBO). A sampler is expected to have a 'sample_qubo'
        and 'sample_ising' method. A sampler is expected to return an
        iterable of samples, in order of increasing energy. If no
        sampler is provided, one must be provided using the
        `set_default_sampler` function.

    sampler_args
        Additional keyword parameters are passed to the sampler.

    Returns
    -------
    vertex_cover : list
       List of nodes that form a minimum vertex cover, as
       determined by the given sampler.

    Examples
    --------
    This example uses a sampler from
    `dimod <https://github.com/dwavesystems/dimod>`_ to find a minimum vertex
    cover for a Chimera unit cell. Both the horizontal (vertices 0,1,2,3) and
    vertical (vertices 4,5,6,7) tiles connect to all 16 edges, so repeated
    executions can return either set.

    >>> import dwave_networkx as dnx
    >>> import dimod
    >>> sampler = dimod.ExactSolver()  # small testing sampler
    >>> G = dnx.chimera_graph(1, 1, 4)
    >>> G.remove_node(7)  # to give a unique solution
    >>> dnx.min_vertex_cover(G, sampler)
    [4, 5, 6]

    Notes
    -----
    Samplers by their nature may not return the optimal solution. This
    function does not attempt to confirm the quality of the returned
    sample.

    References
    ----------
    https://en.wikipedia.org/wiki/Vertex_cover

    https://en.wikipedia.org/wiki/Quadratic_unconstrained_binary_optimization

    .. [AL] Lucas, A. (2014). Ising formulations of many NP problems.
       Frontiers in Physics, Volume 2, Article 5.

    """
    indep_nodes = set(maximum_independent_set(G, sampler, **sampler_args))
    return [v for v in G if v not in indep_nodes]


def is_vertex_cover(G, vertex_cover):
    """Determines whether the given set of vertices is a vertex cover of graph G.

    A vertex cover is a set of vertices such that each edge of the graph
    is incident with at least one vertex in the set.

    Parameters
    ----------
    G : NetworkX graph
       The graph on which to check the vertex cover.

    vertex_cover :
       Iterable of nodes.

    Returns
    -------
    is_cover : bool
        True if the given iterable forms a vertex cover.

    Examples
    --------
    This example checks two covers for a graph, G, of a single Chimera
    unit cell. The first uses the set of the four horizontal qubits, which
    do constitute a cover; the second set removes one node.

    >>> import dwave_networkx as dnx
    >>> G = dnx.chimera_graph(1, 1, 4)
    >>> cover = [0, 1, 2, 3]
    >>> dnx.is_vertex_cover(G,cover)
    True
    >>> cover = [0, 1, 2]
    >>> dnx.is_vertex_cover(G,cover)
    False

    """
    cover = set(vertex_cover)
    return all(u in cover or v in cover for u, v in G.edges)
