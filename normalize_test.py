import normalize as n
import unittest

class TestNormalize(unittest.TestCase):

    def setUp(self):
        self.c_in_c = {"st": 8  ,  "pitch": 60,  "dur": 4 ,  "keysig": 0,  "timesig": 12,  "fermata": 0}
        self.g_in_ab = {"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 16,  "fermata": 0}

    def test_pitch(self):
        self.assertEqual(n.normalize_pitch(self.c_in_c), 0)
        self.assertEqual(self.c_in_c["norm_pitch"], 0)
        
        self.assertEqual(n.normalize_pitch(self.g_in_ab), 11)
        self.assertEqual(self.g_in_ab["norm_pitch"], 11)
      
    def test_dur(self):
        self.assertEqual(n.normalize_dur(self.c_in_c), 1.0/3)
        self.assertEqual(self.c_in_c["norm_dur"], 1.0/3)
        
        self.assertEqual(n.normalize_dur(self.g_in_ab), 1.0/4)
        self.assertEqual(self.g_in_ab["norm_dur"], 1.0/4)

if __name__ == '__main__':
    unittest.main()

