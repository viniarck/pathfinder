"""Main module of kytos/pathfinder Kytos Network Application."""

from flask import jsonify, request
from kytos.core import KytosNApp, log, rest
from kytos.core.helpers import listen_to

# pylint: disable=import-error
from werkzeug.exceptions import BadRequest
from napps.kytos.pathfinder.graph import KytosGraph


class Main(KytosNApp):
    """
    Main class of kytos/pathfinder NApp.

    This class is the entry point for this napp.
    """

    def setup(self):
        """Create a graph to handle the nodes and edges."""
        self.graph = KytosGraph()
        self._topology = None

    def execute(self):
        """Do nothing."""

    def shutdown(self):
        """Shutdown the napp."""

    def _filter_paths(self, paths, desired, undesired):
        """
        Apply filters to the paths list.

        Make sure that each path in the list has all the desired links and none
        of the undesired ones.
        """
        filtered_paths = []

        if desired:
            for link_id in desired:
                try:
                    endpoint_a = self._topology.links[link_id].endpoint_a.id
                    endpoint_b = self._topology.links[link_id].endpoint_b.id
                except KeyError:
                    return []

                for path in paths:
                    head = path["hops"][:-1]
                    tail = path["hops"][1:]
                    if ((endpoint_a, endpoint_b) in zip(head, tail)) or (
                        (endpoint_b, endpoint_a) in zip(head, tail)
                    ):
                        filtered_paths.append(path)
        else:
            filtered_paths = paths

        if undesired:
            for link_id in undesired:
                try:
                    endpoint_a = self._topology.links[link_id].endpoint_a.id
                    endpoint_b = self._topology.links[link_id].endpoint_b.id
                except KeyError:
                    continue

                for path in paths:
                    head = path["hops"][:-1]
                    tail = path["hops"][1:]
                    if ((endpoint_a, endpoint_b) in zip(head, tail)) or (
                        (endpoint_b, endpoint_a) in zip(head, tail)
                    ):

                        filtered_paths.remove(path)

        return filtered_paths

    @rest("v2/", methods=["POST"])
    def shortest_path(self):
        """Calculate the best path between the source and destination."""
        data = request.get_json()

        desired = data.get("desired_links")
        undesired = data.get("undesired_links")
        parameter = data.get("parameter")
        spf_attr = data.get("spf_attribute")

        if not spf_attr:
            spf_attr = parameter or "weight"

        if spf_attr not in self.graph._spf_edge_data_cbs:
            raise BadRequest(
                "Invalid 'spf_attribute'. Valid values: "
                f"{', '.join(self.graph._spf_edge_data_cbs.keys())}"
            )

        paths = self.graph._path_cost_builder(
            self.graph.shortest_paths(
                data["source"],
                data["destination"],
                weight=self.graph._spf_edge_data_cbs[spf_attr],
            ),
            weight=spf_attr
        )

        paths = self._filter_paths(paths, desired, undesired)
        return jsonify({"paths": paths})

    @listen_to("kytos.topology.updated")
    def update_topology(self, event):
        """
        Update the graph when the network topology was updated.

        Clear the current graph and create a new with the most topology updated.
        """
        if "topology" not in event.content:
            return
        try:
            topology = event.content["topology"]
            self._topology = topology
            self.graph.update_topology(topology)
            log.debug("Topology graph updated.")
        except TypeError as err:
            log.debug(err)
        except Exception as err:
            log.debug(err)
