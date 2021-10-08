"""Module to test the KytosGraph in graph.py."""
from itertools import combinations

# Core modules to import
from kytos.core.link import Link

# module under test
from tests.integration.test_results import TestResults


class TestResultsEdges(TestResults):
    """Tests for the graph class.

    Tests to see if reflexive searches and impossible searches
    show correct results.
    """

    def test_path1(self):
        """Tests paths between all users using unconstrained path algorithm."""
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        valid = True
        for point_a, point_b in combos:
            results = self.get_path(point_a, point_b)
            if not results:
                valid = False
                break

        self.assertNotEqual(valid, False)

    def test_path12(self):
        """Tests paths between all users using unconstrained path algorithm."""
        combos = combinations(["User1", "User2", "User3", "User4", "User5"], 2)
        self.initializer()

        valid = True
        for point_a, point_b in combos:
            results = self.get_path(point_a, point_b)
            if not results:
                valid = False
                break

        self.assertEqual(valid, False)

    def test_path2(self):
        """Tests paths between all users using constrained path algorithm,
        with no constraints set.
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for point_a, point_b in combos:
            results = self.get_path_constrained(point_a, point_b)
            self.assertNotEqual(results, [])

    def paths_between_all_users(self, item, base=None, flexible=None, metrics=None):
        """Method to verify the existence of a path between
        a set of points given different constrains"""
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        valid = True
        for point_a, point_b in combos:
            if base is not None and flexible is None:
                results = self.get_path_constrained(
                    point_a, point_b, base=base)
                for result in results:
                    for path in result["paths"]:
                        if item in path:
                            valid = False

            elif base is None and flexible is not None:
                results = self.get_path_constrained(
                    point_a, point_b, flexible=flexible)
                for result in results:
                    if metrics is not None:
                        if metrics in result["metrics"]:
                            for path in result["paths"]:
                                if item in path:
                                    valid = False
                    else:
                        for path in result["paths"]:
                            if item in path:
                                valid = False
        return valid

    def test_path3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S4:1", {'ownership': "B"}))

    def test_path3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S5:2", {'ownership': "B"}))

    def test_path3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S4:2", {'ownership': "B"}))

    def test_path3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("User1:2", {'ownership': "B"}))

    def test_path3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S5:4", {'ownership': "B"}))

    def test_path3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S6:2", {'ownership': "B"}))

    def test_path3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S6:5", {'ownership': "B"}))

    def test_path3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S10:1", {'ownership': "B"}))

    def test_path3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S8:6", {'ownership': "B"}))

    def test_path3_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S10:2", {'ownership': "B"}))

    def test_path3_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("S10:3", {'ownership': "B"}))

    def test_path3_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the ownership constraint set to B.
        """
        self.assertTrue(self.paths_between_all_users("User2:1", {'ownership': "B"}))

    def test_path4_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S4:1", {'reliability': 3}))

    def test_path4_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S5:2", {'reliability': 3}))

    def test_path4_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S5:3", {'reliability': 3}))

    def test_path4_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S6:1", {'reliability': 3}))

    def test_path5_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S3:1", {'bandwidth': 100}))

    def test_path5_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("S5:1", {'bandwidth': 100}))

    def test_path5_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("User1:4", {'bandwidth': 100}))

    def test_path5_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the reliability constraint set to 3.
        """
        self.assertTrue(self.paths_between_all_users("User4:3", {'bandwidth': 100}))

    def test_path6_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S1:1", {'delay': 50}))

    def test_path6_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S2:1", {'delay': 50}))

    def test_path6_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S3:1", {'delay': 50}))

    def test_path6_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S5:1", {'delay': 50}))

    def test_path6_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S4:2", {'delay': 50}))

    def test_path6_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User1:2", {'delay': 50}))

    def test_path6_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S5:5", {'delay': 50}))

    def test_path6_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S8:2", {'delay': 50}))

    def test_path6_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S5:6", {'delay': 50}))

    def test_path6_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User1:3", {'delay': 50}))

    def test_path6_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:3", {'delay': 50}))

    def test_path6_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S9:1", {'delay': 50}))

    def test_path6_1_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:4", {'delay': 50}))

    def test_path6_1_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S9:2", {'delay': 50}))

    def test_path6_1_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50}))

    def test_path6_1_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50}))

    def test_path6_1_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S10:1", {'delay': 50}))

    def test_path6_1_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S8:5", {'delay': 50}))

    def test_path6_1_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("S9:4", {'delay': 50}))

    def test_path6_2_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User1:4", {'delay': 50}))

    def test_path6_2_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50.
        """
        self.assertTrue(self.paths_between_all_users("User4:3", {'delay': 50}))

    def test_path7_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S1:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S2:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S3:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S4:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:2", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:6", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:3", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:3", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:4", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S10:1", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_1_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:4", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_1_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:4", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User4:3", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S3:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S5:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User1:4", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User4:3", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_2_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S4:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:3", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S6:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_2_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:1", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User1:2", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path7_3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:4", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:2", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:5", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:1", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S8:6", {'delay': 50,
                                                              'bandwidth': 100,
                                                              'ownership': "B"}))

    def test_path7_3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:2", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:3", {'delay': 50,
                                                               'bandwidth': 100,
                                                               'ownership': "B"}))

    def test_path7_4_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint set
        to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User2:1", {'delay': 50,
                                                                 'bandwidth': 100,
                                                                 'ownership': "B"}))

    def test_path8_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S1:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S2:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S3:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S4:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:2", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S5:6", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:3", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:3", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:4", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S6:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S10:1", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S8:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("S9:4", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_1_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User1:4", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_2_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # delay = 50
        self.assertTrue(self.paths_between_all_users("User4:3", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='delay'))

    def test_path8_2_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S3:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("S5:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User1:4", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # bandwidth = 100
        self.assertTrue(self.paths_between_all_users("User4:3", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"},
                                                     metrics='bandwidth'))

    def test_path8_2_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S4:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S5:3", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # reliability = 3
        self.assertTrue(self.paths_between_all_users("S6:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"},
                                                     metrics='reliability'))

    def test_path8_2_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:1", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_1(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S4:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_2(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User1:2", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"}))

    def test_path8_3_3(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S5:4", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_4(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:2", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_5(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S6:5", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_6(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:1", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"}))

    def test_path8_3_7(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S8:6", flexible={'delay': 50,
                                                                       'bandwidth': 100,
                                                                       'reliability': 3,
                                                                       'ownership': "B"}))

    def test_path8_3_8(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:2", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"}))

    def test_path8_3_9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("S10:3", flexible={'delay': 50,
                                                                        'bandwidth': 100,
                                                                        'reliability': 3,
                                                                        'ownership': "B"}))

    def test_path8_4_0(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with flexibility enabled
        """
        # ownership = "B"
        self.assertTrue(self.paths_between_all_users("User2:1", flexible={'delay': 50,
                                                                          'bandwidth': 100,
                                                                          'reliability': 3,
                                                                          'ownership': "B"}))

    def test_path9(self):
        """Tests paths between all users using constrained path algorithm,
        with the delay constraint set to 50, the bandwidth constraint
        set to 100, the reliability constraint set to 3, and the ownership
        constraint set to 'B'

        Tests conducted with all but ownership flexible
        """
        combos = combinations(["User1", "User2", "User3", "User4"], 2)
        self.initializer()

        for point_a, point_b in combos:
            results = self.get_path_constrained(point_a, point_b,
                                                base={"ownership": "B"},
                                                flexible={"delay": 50,
                                                          "bandwidth": 100,
                                                          "reliability": 3})
            for result in results:
                # delay = 50 checks
                if "delay" in result["metrics"]:
                    for path in result["paths"]:
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
                if "bandwidth" in result["metrics"]:
                    for path in result["paths"]:
                        self.assertNotIn("S3:1", path)
                        self.assertNotIn("S5:1", path)
                        self.assertNotIn("User1:4", path)
                        self.assertNotIn("User4:3", path)

                # reliability = 3 checks
                if "reliability" in result["metrics"]:
                    for path in result["paths"]:
                        self.assertNotIn("S4:1", path)
                        self.assertNotIn("S5:2", path)
                        self.assertNotIn("S5:3", path)
                        self.assertNotIn("S6:1", path)

                # ownership = "B" checks
                self.assertIn("ownership", result["metrics"])
                for path in result["paths"]:
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
        """Tests that TypeError is generated by get_path_constrained

        Tests with ownership using an int type rather than string
        """
        self.initializer()

        with self.assertRaises(TypeError):
            self.get_path_constrained(
                "User1", "User2", base={"ownership": 1})

    @staticmethod
    def generate_topology():
        """Generates a predetermined topology"""
        switches = {}
        interfaces = {}
        links = {}

        TestResults.create_switch("S1", switches)
        TestResults.add_interfaces(2, switches["S1"], interfaces)

        TestResults.create_switch("S2", switches)
        TestResults.add_interfaces(2, switches["S2"], interfaces)

        TestResults.create_switch("S3", switches)
        TestResults.add_interfaces(6, switches["S3"], interfaces)

        TestResults.create_switch("S4", switches)
        TestResults.add_interfaces(2, switches["S4"], interfaces)

        TestResults.create_switch("S5", switches)
        TestResults.add_interfaces(6, switches["S5"], interfaces)

        TestResults.create_switch("S6", switches)
        TestResults.add_interfaces(5, switches["S6"], interfaces)

        TestResults.create_switch("S7", switches)
        TestResults.add_interfaces(2, switches["S7"], interfaces)

        TestResults.create_switch("S8", switches)
        TestResults.add_interfaces(8, switches["S8"], interfaces)

        TestResults.create_switch("S9", switches)
        TestResults.add_interfaces(4, switches["S9"], interfaces)

        TestResults.create_switch("S10", switches)
        TestResults.add_interfaces(3, switches["S10"], interfaces)

        TestResults.create_switch("S11", switches)
        TestResults.add_interfaces(3, switches["S11"], interfaces)

        TestResults.create_switch("User1", switches)
        TestResults.add_interfaces(4, switches["User1"], interfaces)

        TestResults.create_switch("User2", switches)
        TestResults.add_interfaces(2, switches["User2"], interfaces)

        TestResults.create_switch("User3", switches)
        TestResults.add_interfaces(2, switches["User3"], interfaces)

        TestResults.create_switch("User4", switches)
        TestResults.add_interfaces(3, switches["User4"], interfaces)

        TestResultsEdges._fill_links(links, interfaces)

        TestResultsEdges._add_metadata_to_links(links)

        return switches, links

    @staticmethod
    def _add_metadata_to_links(links):
        links["S1:1<->S2:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 105})

        links["S1:2<->User1:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S2:2<->User4:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 10})

        links["S3:1<->S5:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 10, "delay": 112})

        links["S3:2<->S7:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S3:3<->S8:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S3:4<->S11:1"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 6})

        links["S3:5<->User3:1"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S3:6<->User4:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 10})

        links["S4:1<->S5:2"].extend_metadata(
            {"reliability": 1, "bandwidth": 100, "delay": 30,
             "ownership": "A"})

        links["S4:2<->User1:2"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 110,
             "ownership": "A"})

        links["S5:3<->S6:1"].extend_metadata(
            {"reliability": 1, "bandwidth": 100, "delay": 40})

        links["S5:4<->S6:2"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 40,
             "ownership": "A"})

        links["S5:5<->S8:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 112})

        links["S5:6<->User1:3"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 60})

        links["S6:3<->S9:1"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 60})

        links["S6:4<->S9:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 62})

        links["S6:5<->S10:1"].extend_metadata(
            {"bandwidth": 100, "delay": 108, "ownership": "A"})

        links["S7:2<->S8:3"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S8:4<->S9:3"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 32})

        links["S8:5<->S9:4"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 110})

        links["S8:6<->S10:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "ownership": "A"})

        links["S8:7<->S11:2"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 7})

        links["S8:8<->User3:2"].extend_metadata(
            {"reliability": 5, "bandwidth": 100, "delay": 1})

        links["S10:3<->User2:1"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 10,
             "ownership": "A"})

        links["S11:3<->User2:2"].extend_metadata(
            {"reliability": 3, "bandwidth": 100, "delay": 6})

        links["User1:4<->User4:3"].extend_metadata(
            {"reliability": 5, "bandwidth": 10, "delay": 105})

    @staticmethod
    def _fill_links(links, interfaces):
        links["S1:1<->S2:1"] = Link(interfaces["S1:1"], interfaces["S2:1"])

        links["S1:2<->User1:1"] = Link(interfaces["S1:2"], interfaces["User1:1"])

        links["S2:2<->User4:1"] = Link(interfaces["S2:2"], interfaces["User4:1"])

        links["S3:1<->S5:1"] = Link(interfaces["S3:1"], interfaces["S5:1"])

        links["S3:2<->S7:1"] = Link(interfaces["S3:2"], interfaces["S7:1"])

        links["S3:3<->S8:1"] = Link(interfaces["S3:3"], interfaces["S8:1"])

        links["S3:4<->S11:1"] = Link(interfaces["S3:4"], interfaces["S11:1"])

        links["S3:5<->User3:1"] = Link(interfaces["S3:5"], interfaces["User3:1"])

        links["S3:6<->User4:2"] = Link(interfaces["S3:6"], interfaces["User4:2"])

        links["S4:1<->S5:2"] = Link(interfaces["S4:1"], interfaces["S5:2"])

        links["S4:2<->User1:2"] = Link(interfaces["S4:2"], interfaces["User1:2"])

        links["S5:3<->S6:1"] = Link(interfaces["S5:3"], interfaces["S6:1"])

        links["S5:4<->S6:2"] = Link(interfaces["S5:4"], interfaces["S6:2"])

        links["S5:5<->S8:2"] = Link(interfaces["S5:5"], interfaces["S8:2"])

        links["S5:6<->User1:3"] = Link(interfaces["S5:6"], interfaces["User1:3"])

        links["S6:3<->S9:1"] = Link(interfaces["S6:3"], interfaces["S9:1"])

        links["S6:4<->S9:2"] = Link(interfaces["S6:4"], interfaces["S9:2"])

        links["S6:5<->S10:1"] = Link(interfaces["S6:5"], interfaces["S10:1"])

        links["S7:2<->S8:3"] = Link(interfaces["S7:2"], interfaces["S8:3"])

        links["S8:4<->S9:3"] = Link(interfaces["S8:4"], interfaces["S9:3"])

        links["S8:5<->S9:4"] = Link(interfaces["S8:5"], interfaces["S9:4"])

        links["S8:6<->S10:2"] = Link(interfaces["S8:6"], interfaces["S10:2"])

        links["S8:7<->S11:2"] = Link(interfaces["S8:7"], interfaces["S11:2"])

        links["S8:8<->User3:2"] = Link(interfaces["S8:8"], interfaces["User3:2"])

        links["S10:3<->User2:1"] = Link(interfaces["S10:3"], interfaces["User2:1"])

        links["S11:3<->User2:2"] = Link(interfaces["S11:3"], interfaces["User2:2"])

        links["User1:4<->User4:3"] = Link(interfaces["User1:4"], interfaces["User4:3"])
