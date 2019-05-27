import unittest
import bees

class testBeesMethods(unittest.TestCase):

    def testMakeTable(self):
        data = [[0,0,0], [1,3,4], [2,-3,4], [3,-3,-4]]
        expected_table = [[0.0, 5.0, 5.0, 5.0], [5.0, 0.0, 6.0, 10.0], [5.0, 6.0, 0.0, 8.0], [5.0, 10.0, 8.0, 0.0]]

        table = bees.make_distance_table(data)
        self.assertEqual(table, expected_table)

    def testGetTotalDistanceOfPath(self):
        path = [0,1,2,3]
        table = [
                [0.0, 5.0, 5.0, 5.0],
                [5.0, 0.0, 6.0, 10.0],
                [5.0, 6.0, 0.0, 8.0],
                [5.0, 10.0, 8.0, 0.0]]
        expected_distance = 24.0

        distance = bees.get_total_distance_of_path(path, table)
        self.assertEqual(distance, expected_distance)




if __name__ == '__main__':
    unittest.main()
