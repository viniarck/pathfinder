"""Module to test the KytosGraph in graph.py."""

from tests.integration.metadata_settings import MetadataSettings


class TestPathsMetadata(MetadataSettings):
    """Tests for the graph class.

    Tests if the metadata in search result edges have passing values.
    """

    def test_path_constrained_user_user(self):
        """Test to see if there is a constrained
        path between User - User."""
        self.initializer()
        result = self.get_path_constrained("User1", "User2")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_user_switch(self):
        """Test to see if there is a constrained
        path between User - Switch."""
        self.initializer()
        result = self.get_path_constrained("User1", "S4")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_switch_switch(self):
        """Test to see if there is a constrained
        path between Switch - Switch."""
        self.initializer()
        result = self.get_path_constrained("S2", "S4")
        self.assertNotEqual(result, [], True)

    def test_no_path_constrained_user_user(self):
        """Test to see if there is NOT a constrained
        path between User - User."""
        self.initializer()
        result = self.get_path_constrained("User1", "User3")
        self.assertEqual(result, [], True)

    def test_path_constrained_user_user_t1(self):
        """Test to see if there is a constrained path between
        User - User using the 2nd topology variant."""
        self.initializer(val=1)
        result = self.get_path_constrained("User1", "User3")
        self.assertNotEqual(result, [], True)

    def test_no_path_constrained_user_user_t1(self):
        """Test to see if there is NOT a constrained path between
        User - User using the 2nd topology variant."""
        self.initializer(val=1)
        result = self.get_path_constrained("User1", "User2")
        self.assertEqual(result, [], True)

    def test_no_path_constrained_switch_switch_t1(self):
        """Test to see if there is NOT a constrained path between
        Switch - Switch using the 2nd topology variant."""
        self.initializer(val=1)
        result = self.get_path_constrained("S1", "S2")
        self.assertEqual(result, [], True)

    def test_path_constrained_user_user_t2(self):
        """Test to see if there is a constrained path between
        User - User using the 3rd topology variant."""
        self.initializer(val=2)
        result = self.get_path_constrained("User1", "User2")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_user_switch_t2(self):
        """Test to see if there is a constrained path between
        User - Switch using the 3rd topology variant."""
        self.initializer(val=2)
        result = self.get_path_constrained("User1", "S4")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_switch_switch_t2(self):
        """Test to see if there is a constrained path between
        two switches using the 3rd topology variant."""
        self.initializer(val=2)
        result = self.get_path_constrained("S2", "S4")
        self.assertNotEqual(result, [], True)

    def test_path_constrained_reliability(self):
        """Tests to see if the edges used in the paths
        of the result set do not have poor reliability
        """
        requirements = {"reliability": 3}

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        self.assertNotEqual(result, [])

    def test_no_path_constrained_reliability(self):
        """Tests to see if the edges used in the paths
        of the result set do not have poor reliability
        """
        requirements = {"reliability": 3}

        self.initializer()

        result = self.get_path_constrained("User1", "User3", base=requirements)

        self.assertEqual(result, [])

    def test_path_constrained_reliability_detailed(self):
        """Tests to see if the edges used in the paths
        of the result set do not have poor reliability
        """
        reliabilities = []
        requirements = {"reliability": 3}
        poor_reliability = 1

        self.initializer()

        result = self.get_path_constrained("User1", "User2", base=requirements)

        if result:
            for path in result[0]["hops"]:
                for i in range(1, len(path)):
                    endpoint_a = path[i - 1]
                    endpoint_b = path[i]
                    meta_data = self.graph.get_link_metadata(endpoint_a, endpoint_b)
                    if meta_data and "reliability" in meta_data.keys():
                        reliabilities.append(meta_data["reliability"])

            self.assertNotIn(poor_reliability, reliabilities)

        else:
            self.assertNotEqual(result, [])

    def test_path_constrained_delay(self):
        """Tests to see if the edges used in the paths
        from User 1 to User 2 have less than 30 delay.
        """
        delays = []
        requirements = {"delay": 29}

        self.initializer()

        paths = self.get_path_constrained("User1", "User2", base=requirements)
        assert paths

        for path in paths:
            for i, j in zip(
                range(0, len(path["hops"])), range(1, len(path["hops"]))
            ):
                endpoint_a = path["hops"][i]
                endpoint_b = path["hops"][j]
                meta_data = self.graph.get_link_metadata(endpoint_a, endpoint_b)
                if meta_data and "delay" in meta_data.keys():
                    delays.append(meta_data["delay"])

        assert delays
        for delay in delays:
            assert delay <= requirements["delay"]

    def links_metadata_values(self, path, attr):
        """Method to build a list of metadata values of the links of a path"""
        values = []
        for i, j in zip(
            range(0, len(path["hops"])), range(1, len(path["hops"]))
        ):
            endpoint_a = path["hops"][i]
            endpoint_b = path["hops"][j]
            meta_data = self.graph.get_link_metadata(endpoint_a, endpoint_b)
            if meta_data and attr in meta_data.keys():
                values.append(meta_data[attr])
        return values

    def test_path_constrained_bandwidth_detailed(self):
        """Tests to see if the edges used in the paths
        from User 1 to User 2 have at least 20 bandwidth.
        """
        requirements = {"bandwidth": 20}

        self.initializer()

        paths = self.get_path_constrained("User1", "User2", base=requirements)
        assert paths

        for path in paths:
            bandwidths = self.links_metadata_values(path, "bandwidth")
            assert bandwidths

            for bandwidth in bandwidths:
                assert bandwidth >= requirements["bandwidth"]

    def test_path_constrained_bandwidth_detailed_t2(self):
        """Tests to see if the edges used in the paths
        from User 1 to User 2 have at least 20 bandwidth.
        """
        requirements = {"bandwidth": 20}

        self.initializer(val=2)

        paths = self.get_path_constrained("User1", "User2", base=requirements)
        assert paths

        for path in paths:
            bandwidths = self.links_metadata_values(path, "bandwidth")
            assert bandwidths
            for bandwidth in bandwidths:
                assert bandwidth >= requirements["bandwidth"]

    def test_path_constrained_bandwidth_delay(self):
        """Tests to see if the edges used in the paths from User 1
        to User 2 have at least 20 bandwidth and under 30 delay.
        """
        requirements = {"bandwidth": 20, "delay": 29}

        self.initializer()

        paths = self.get_path_constrained("User1", "User2", base=requirements)
        assert paths

        for path in paths:

            bandwidths = self.links_metadata_values(path, "bandwidth")
            assert bandwidths
            for bandwidth in bandwidths:
                assert bandwidth >= requirements["bandwidth"]

            delays = self.links_metadata_values(path, "delay")
            assert delays
            for delay in delays:
                assert delay <= requirements["delay"]

            assert len(bandwidths) == len(delays)
