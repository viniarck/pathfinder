"""Module Graph of kytos/pathfinder Kytos Network Application."""

from itertools import combinations

from kytos.core import log

try:
    import networkx as nx
    from networkx.exception import NodeNotFound, NetworkXNoPath
except ImportError:
    PACKAGE = 'networkx>=2.2'
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")
try:
    from exactdelaypathfinder.core import ExactDelayPathfinder
except ImportError:
    PACKAGE = 'exactdelaypathfinder>=0.1.0'
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")


class Filter:
    """Class responsible for removing items with disqualifying values."""

    def __init__(self, filter_type, filter_function):
        self._filter_type = filter_type
        self._filter_function = filter_function

    def run(self, value, items):
        """Filter out items."""
        if isinstance(value, self._filter_type):
            return filter(self._filter_function(value), items)

        raise TypeError(f"Expected type: {self._filter_type}")


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()
        self._filter_functions = {}

        def filter_leq(metric):  # Lower values are better
            return lambda x: (lambda y: y[2].get(metric, x) <= x)

        def filter_geq(metric):  # Higher values are better
            return lambda x: (lambda y: y[2].get(metric, x) >= x)

        def filter_eeq(metric):  # Equivalence
            return lambda x: (lambda y: y[2].get(metric, x) == x)

        self._filter_functions["ownership"] = Filter(
            str, filter_eeq("ownership"))

        self._filter_functions["bandwidth"] = Filter(
            (int, float), filter_geq("bandwidth"))

        self._filter_functions["priority"] = Filter(
            (int, float), filter_geq("priority"))

        self._filter_functions["reliability"] = Filter(
            (int, float), filter_geq("reliability"))

        self._filter_functions["utilization"] = Filter(
            (int, float), filter_leq("utilization"))

        self._filter_functions["delay"] = Filter(
            (int, float), filter_leq("delay"))

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
        for hop in circuit['hops']:
            if len(hop.split(':')) == 8:
                circuit['hops'].remove(hop)

    def shortest_paths(self, source, destination, parameter=None):
        """Calculate the shortest paths and return them."""
        try:
            paths = list(nx.shortest_simple_paths(self.graph,
                                                  source, destination,
                                                  parameter))
        except (NodeNotFound, NetworkXNoPath):
            return []
        return paths

    def exact_path(self, total_delay, source, destination):
        """Obtain paths with total delays equal or close to the user's requirements.

        This function utilizes the ExactDelayPathfinder
        library developed by the AmLight team at FIU.
        """
        pathfinder = ExactDelayPathfinder()
        result = pathfinder.search(self.graph, total_delay, source, destination)
        return result

    def constrained_flexible_paths(self, source, destination,
                                   minimum_hits=None, **metrics):
        """Calculate the constrained shortest paths with flexibility."""
        base = metrics.get("base", {})
        flexible = metrics.get("flexible", {})
        first_pass_links = list(self._filter_links(self.graph.edges(data=True),
                                                   **base))
        length = len(flexible)
        if minimum_hits is None:
            # minimum_hits = length
            minimum_hits = 0
        minimum_hits = min(length, max(0, minimum_hits))
        # minimum_hits = max(minimum_hits, 0)
        results = []
        paths = []
        # i = minimum_hits
        # i = 0
        # while paths == [] and i <= length:
        for i in range(length, minimum_hits - 1, -1):
            for combo in combinations(flexible.items(), i):
                additional = dict(combo)
                paths = self._constrained_shortest_paths(
                    source, destination,
                    self._filter_links(first_pass_links,
                                       metadata=False, **additional))
                if paths:
                    results.append(
                        {"paths": paths, "metrics": {**base, **additional}})
            # i = i + 1
            if paths:
                break
        return results

    def _constrained_shortest_paths(self, source, destination, links):
        paths = []
        try:
            paths = list(self._path_function(self.graph.edge_subgraph(links),
                                             source, destination))
        except NetworkXNoPath:
            pass
        except NodeNotFound:
            if source == destination:
                if source in self.graph.nodes:
                    paths = [[source]]
        return paths

    def _filter_links(self, links, metadata=True, **metrics):
        for metric, value in metrics.items():
            filter_ = self._filter_functions.get(metric, None)
            if filter_ is not None:
                try:
                    links = filter_.run(value, links)
                except TypeError as err:
                    raise TypeError(f"Error in {metric} value: {err}")
        if not metadata:
            links = ((u, v) for u, v, d in links)
        return links

    def get_nodes(self):
        return self.graph.nodes

    def get_edges(self):
        return self.graph.edges
