"""Module Graph of kytos/pathfinder Kytos Network Application."""

from itertools import combinations

from kytos.core import log

try:
    import networkx as nx
    from networkx.exception import NodeNotFound, NetworkXNoPath
except ImportError:
    PACKAGE = "networkx>=2.2"
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")


def lazy_filter(filter_type, filter_function):
    """Lazy typed filter on top of the built-in function, it's meant
    to be used when the values to be filtered for are only defined later on
    dynamically at runtime."""

    def filter_closure(value, items):
        if not isinstance(value, filter_type):
            raise TypeError(f"Expected type: {filter_type}")
        return filter(filter_function(value), items)

    return filter_closure


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()
        self._filter_functions = {}

        def filter_le(metric):
            return lambda x: (lambda nx_edge_tup: nx_edge_tup[2].get(metric, x) <= x)

        def filter_ge(metric):
            return lambda x: (lambda nx_edge_tup: nx_edge_tup[2].get(metric, x) >= x)

        def filter_in(metric):
            return lambda x: (lambda nx_edge_tup: x in nx_edge_tup[2].get(metric, {x}))

        self._filter_functions["ownership"] = lazy_filter(str, filter_in("ownership"))

        self._filter_functions["bandwidth"] = lazy_filter(
            (int, float), filter_ge("bandwidth")
        )

        self._filter_functions["reliability"] = lazy_filter(
            (int, float), filter_ge("reliability")
        )

        self._filter_functions["priority"] = lazy_filter(
            (int, float), filter_le("priority")
        )

        self._filter_functions["utilization"] = lazy_filter(
            (int, float), filter_le("utilization")
        )

        self._filter_functions["delay"] = lazy_filter((int, float), filter_le("delay"))

        self._path_function = nx.all_shortest_paths

    def clear(self):
        """
        Remove all nodes and links registered.
        """
        self.graph.clear()

    def update_topology(self, topology):
        """Update all nodes and links inside the graph."""
        self.graph.clear()
        self.update_nodes(topology.switches)
        self.update_links(topology.links)

    def update_nodes(self, nodes):
        """Update all nodes inside the graph."""
        for node in nodes.values():
            try:
                self.graph.add_node(node.id)

                for interface in node.interfaces.values():
                    self.graph.add_node(interface.id)
                    self.graph.add_edge(node.id, interface.id)

            except AttributeError:
                raise TypeError("Problems encountered updating nodes inside the graph")

    def update_links(self, links):
        """Update all links inside the graph."""
        for link in links.values():
            if link.is_active():
                self.graph.add_edge(link.endpoint_a.id, link.endpoint_b.id)
                for key, value in link.metadata.items():
                    endpoint_a = link.endpoint_a.id
                    endpoint_b = link.endpoint_b.id
                    self.graph[endpoint_a][endpoint_b][key] = value

    def get_link_metadata(self, endpoint_a, endpoint_b):
        """Return the metadata of a link."""
        return self.graph.get_edge_data(endpoint_a, endpoint_b)

    @staticmethod
    def _remove_switch_hops(circuit):
        """Remove switch hops from a circuit hops list."""
        for hop in circuit["hops"]:
            if len(hop.split(":")) == 8:
                circuit["hops"].remove(hop)

    def shortest_paths(self, source, destination, parameter=None):
        """Calculate the shortest paths and return them."""
        try:
            paths = list(
                nx.shortest_simple_paths(self.graph, source, destination, parameter)
            )
        except (NodeNotFound, NetworkXNoPath):
            return []
        return paths

    def constrained_flexible_paths(
        self, source, destination, minimum_hits=None, **metrics
    ):
        """Calculate the constrained shortest paths with flexibility."""
        base = metrics.get("base", {})
        flexible = metrics.get("flexible", {})
        first_pass_links = list(self._filter_links(self.graph.edges(data=True), **base))
        length = len(flexible)
        if minimum_hits is None:
            minimum_hits = 0
        minimum_hits = min(length, max(0, minimum_hits))
        paths = []
        for i in range(length, minimum_hits - 1, -1):
            constrained_paths = []
            for combo in combinations(flexible.items(), i):
                additional = dict(combo)
                constrained_paths = self._constrained_shortest_paths(
                    source,
                    destination,
                    self._filter_links(first_pass_links, metadata=False, **additional),
                )
                for path in constrained_paths:
                    paths.append({"hops": path, "metrics": {**base, **additional}})
            if paths:
                break
        return paths

    def _constrained_shortest_paths(self, source, destination, links):
        paths = []
        try:
            paths = list(
                self._path_function(
                    self.graph.edge_subgraph(links), source, destination
                )
            )
        except NetworkXNoPath:
            pass
        except NodeNotFound:
            if source == destination:
                if source in self.graph.nodes:
                    paths = [[source]]
        return paths

    def _filter_links(self, links, metadata=True, **metrics):
        for metric, value in metrics.items():
            filter_func = self._filter_functions.get(metric, None)
            if filter_func is not None:
                try:
                    links = filter_func(value, links)
                except TypeError as err:
                    raise TypeError(f"Error in {metric} value: {err}")
        if not metadata:
            links = ((u, v) for u, v, d in links)
        return links
