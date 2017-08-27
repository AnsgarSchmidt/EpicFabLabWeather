import unittest
from OpenSenseMap import OpenSenseMap

class OpenSenseMapTest(unittest.TestCase):
    def test(self):
        open_sense_map = OpenSenseMap({"davis/outTemp_C":"12.0"})
        url, data = open_sense_map.createRequestBody("https://api.opensensemap.org/boxes/", "temperature")
        self.assertEquals(data[0]['value'], 12.00)

if __name__ == '__main__':
    unittest.main()
