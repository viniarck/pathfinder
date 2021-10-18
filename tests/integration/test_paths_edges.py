"""Module to test the KytosGraph in graph.py."""
from itertools import combinations

# module under test
from tests.integration.edges_settings import EdgesSettings


class TestPathsEdges(EdgesSettings):
    """Tests for the graph class.

    Tests to see if reflexive searches and impossible searches
    show correct paths.
    """

    def test_k_shortest_paths_among_users(self):
        """Tests paths between all users using unconstrained path algorithm."""
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.k_shortest_paths(source, destination)
            assert paths
            for path in paths:
                assert path[0] == source
                assert path[-1] == destination

    def test_constrained_k_shortest_paths_among_users(self):
        """Tests paths between all users using constrained path algorithm,
        with no constraints set.
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.constrained_k_shortest_paths(
                source, destination
            )
            assert paths
            for path in paths:
                assert path["hops"][0] == source
                assert path["hops"][-1] == destination

    def test_path3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S4:1", {"ownership": "B"})

    def test_path3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S5:2", {"ownership": "B"})

    def test_path3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S4:2", {"ownership": "B"})

    def test_path3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("User1:2", {"ownership": "B"})

    def test_path3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S5:4", {"ownership": "B"})

    def test_path3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S6:2", {"ownership": "B"})

    def test_path3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S6:5", {"ownership": "B"})

    def test_path3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S10:1", {"ownership": "B"})

    def test_path3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S8:6", {"ownership": "B"})

    def test_path3_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S10:2", {"ownership": "B"})

    def test_path3_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("S10:3", {"ownership": "B"})

    def test_path3_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        assert self.paths_between_all_users("User2:1", {"ownership": "B"})

    def test_path4_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("S4:1", {"reliability": 3})

    def test_path4_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("S5:2", {"reliability": 3})

    def test_path4_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("S5:3", {"reliability": 3})

    def test_path4_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("S6:1", {"reliability": 3})

    def test_path5_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("S3:1", {"bandwidth": 100})

    def test_path5_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("S5:1", {"bandwidth": 100})

    def test_path5_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("User1:4", {"bandwidth": 100})

    def test_path5_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        assert self.paths_between_all_users("User4:3", {"bandwidth": 100})

    def test_path9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with all but ownership flexible
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for source, destination in combos:
            paths = self.graph.constrained_k_shortest_paths(
                source,
                destination,
                mandatory_metrics={"ownership": "B"},
                flexible={"delay": 50, "bandwidth": 100, "reliability": 3},
            )
            for path in paths:
                # delay = 50 checks
                if "delay" in path["metrics"]:
                    for path in path["hops"]:
                        self.assertNotIn("S1:1", path)
                        self.assertNotIn("S2:1", path)
                        self.assertNotIn("S3:1", path)
                        self.assertNotIn("S5:1", path)
                        self.assertNotIn("S4:2", path)
                        self.assertNotIn("User1:2", path)
                        self.assertNotIn("S5:5", path)
                        self.assertNotIn("S8:2", path)
                        self.assertNotIn("S5:6", path)
                        self.assertNotIn("User1:3", path)
                        self.assertNotIn("S6:3", path)
                        self.assertNotIn("S9:1", path)
                        self.assertNotIn("S6:4", path)
                        self.assertNotIn("S9:2", path)
                        self.assertNotIn("S6:5", path)
                        self.assertNotIn("S10:1", path)
                        self.assertNotIn("S8:5", path)
                        self.assertNotIn("S9:4", path)
                        self.assertNotIn("User1:4", path)
                        self.assertNotIn("User4:3", path)

                # bandwidth = 100 checks
                if "bandwidth" in path["metrics"]:
                    for path in path["hops"]:
                        self.assertNotIn("S3:1", path)
                        self.assertNotIn("S5:1", path)
                        self.assertNotIn("User1:4", path)
                        self.assertNotIn("User4:3", path)

                # reliability = 3 checks
                if "reliability" in path["metrics"]:
                    for path in path["hops"]:
                        self.assertNotIn("S4:1", path)
                        self.assertNotIn("S5:2", path)
                        self.assertNotIn("S5:3", path)
                        self.assertNotIn("S6:1", path)

                # ownership = "B" checks
                self.assertIn("ownership", path["metrics"])
                for path in path["hops"]:
                    self.assertNotIn("S4:1", path)
                    self.assertNotIn("S5:2", path)
                    self.assertNotIn("S4:2", path)
                    self.assertNotIn("User1:2", path)
                    self.assertNotIn("S5:4", path)
                    self.assertNotIn("S6:2", path)
                    self.assertNotIn("S6:5", path)
                    self.assertNotIn("S10:1", path)
                    self.assertNotIn("S8:6", path)
                    self.assertNotIn("S10:2", path)
                    self.assertNotIn("S10:3", path)
                    self.assertNotIn("User2:1", path)

    def test_path10(self):
        """Tests that TypeError."""
        self.initializer()

        with self.assertRaises(TypeError):
            self.graph.constrained_k_shortest_paths(
                "User1", "User2", mandatory_metrics={"ownership": 1}
            )
