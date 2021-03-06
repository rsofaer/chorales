#!/usr/bin/python

import chordEnergy as e
import json
import unittest

data = json.load(open("../dataset/cleandata.json", "rb")).values()
def hasKeySig(chorale):
    return not chorale[0][0]["keysig"] == None

data = filter(hasKeySig, data)

class TestChordEnergy(unittest.TestCase):

    def setUp(self):
        self.chorale = data[0]
        self.ce = e.ChordEnergizer([self.chorale])

    def testCopitchMap(self):
        e.copitch_map(e.table_from_chorale(self.chorale))

    def testChordPairEnergy(self):
        self.chorales = data
        self.ce = e.ChordEnergizer(self.chorales)
        self.assertTrue(self.ce.pair_energy({e.pitch_key: 0}, {e.pitch_key: 1}) >
                        self.ce.pair_energy({e.pitch_key: 0}, {e.pitch_key: 3}))

        self.assertTrue(self.ce.pair_energy({e.pitch_key: 0}, {e.pitch_key: 3}) == self.ce.pair_energy(0,3))

        self.assertTrue(self.ce.sum_pair_energy([0,1,2,3]) == self.ce.sum_pair_energy([{e.pitch_key: 0},{e.pitch_key: 1},{e.pitch_key: 2},{e.pitch_key: 3}]))
        self.assertTrue(self.ce.chord_energy([0,1,2,3]) == self.ce.chord_energy([{e.pitch_key: 0},{e.pitch_key: 1},{e.pitch_key: 2},{e.pitch_key: 3}]))
        self.assertTrue(self.ce.chord_pair_energy([0,1,2,3],[1,2,3,4]) == 
                        self.ce.chord_pair_energy([{e.pitch_key: 0},{e.pitch_key: 1},{e.pitch_key: 2},{e.pitch_key: 3}],
                                                  [{e.pitch_key: 1},{e.pitch_key: 2},{e.pitch_key: 3},{e.pitch_key: 4}]))

if __name__ == '__main__':
    unittest.main()

