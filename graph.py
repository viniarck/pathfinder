"""Module Graph of kytos/pathfinder Kytos Network Application."""

from itertools import combinations
from itertools import islice

from kytos.core import log
from napps.kytos.pathfinder.utils import lazy_filter
from napps.kytos.pathfinder.utils import nx_edge_data_delay
from napps.kytos.pathfinder.utils import nx_edge_data_priority
from napps.kytos.pathfinder.utils import nx_edge_data_weight
from napps.kytos.pathfinder.utils import filter_le
from napps.kytos.pathfinder.utils import filter_ge
from napps.kytos.pathfinder.utils import filter_in

try:
    import networkx as nx
    from networkx.exception import NodeNotFound, NetworkXNoPath
except ImportError:
    PACKAGE = "networkx>=2.2"
    log.error(f"Package {PACKAGE} not found. Please 'pip install {PACKAGE}'")


class KytosGraph:
    """Class responsible for the graph generation."""

    def __init__(self):
        self.graph = nx.Graph()
        self._filter_functions = {
            "ownership": lazy_filter(str, filter_in("ownership")),
            "bandwidth": lazy_filter((int, float), filter_ge("bandwidth")),
            "reliability": lazy_filter((int, float), filter_ge("reliability")),
            "priority": lazy_filter((int, float), filter_le("priority")),
            "utilization": lazy_filter((int, float), filter_le("utilization")),
            "delay": lazy_filter((int, float), filter_le("delay")),
        }
        self._spf_edge_data_cbs = {
            "weight": nx_edge_data_weight,
            "delay": nx_edge_data_delay,
            "priority": nx_edge_data_priority,
        }

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

    def _path_cost(self, path, weight="weight", default_cost=1):
        """Compute the path cost given an attribute."""
        cost = 0
        for node, nbr in nx.utils.pairwise(path):
            cost += self.graph[node][nbr].get(weight, default_cost)
        return cost

    def _path_cost_builder(self, paths, weight="weight", default_weight=1):
        """Build the cost of a path given a list of paths."""
        paths_acc = []
        for path in paths:
            if isinstance(path, list):
                paths_acc.append(
                    {
                        "hops": path,
                        "cost": self._path_cost(
                            path, weight=weight, default_cost=default_weight
                        ),
                    }
                )
            elif isinstance(path, dict):
                path["cost"] = self._path_cost(
                    path["hops"], weight=weight, default_cost=default_weight
                )
                paths_acc.append(path)
            else:
                raise TypeError(
                    f"path type: '{type(path)}' must be be either list or dict. "
                    f"path: {path}"
                )
        return paths_acc

    def shortest_paths(self, source, destination, weight=None, k=1):
        """Calculate the shortest paths and return them."""
        try:
            return list(
                islice(
                    nx.shortest_simple_paths(
                        self.graph, source, destination, weight=weight
                    ),
                    k,
                )
            )
        except (NodeNotFound, NetworkXNoPath):
            return []

    def constrained_shortest_paths(
        self, source, destination, minimum_hits=None, weight=None, **metrics
    ):
        """Calculate the constrained shortest paths with flexibility."""
        mandatory_metrics = metrics.get("mandatory_metrics", {})
        flexible_metrics = metrics.get("flexible_metrics", {})
        first_pass_links = list(
            self._filter_links(self.graph.edges(data=True), **mandatory_metrics)
        )
        length = len(flexible_metrics)
        if minimum_hits is None:
            minimum_hits = 0
        minimum_hits = min(length, max(0, minimum_hits))
        paths = []
        for i in range(length, minimum_hits - 1, -1):
            constrained_paths = []
            for combo in combinations(flexible_metrics.items(), i):
                additional = dict(combo)
                constrained_paths = self._constrained_shortest_paths(
                    source,
                    destination,
                    self._filter_links(first_pass_links, metadata=False, **additional),
                    weight=weight,
                )
                for path in constrained_paths:
                    paths.append(
                        {"hops": path, "metrics": {**mandatory_metrics, **additional}}
                    )
            if paths:
                break
        return paths

    def _constrained_shortest_paths(self, source, destination, links, weight=None):
        paths = []
        try:
            paths = list(
                nx.all_shortest_paths(
                    self.graph.edge_subgraph(links), source, destination, weight=weight
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
