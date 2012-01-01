#!/usr/bin/python

import chordEnergy as e
import json
import unittest

data = json.load(open("../dataset/cleandata.json", "rb")).values()
class TestChordEnergy(unittest.TestCase):

    def setUp(self):
        self.chorale = data[0]
        self.ce = e.ChordEnergizer([self.chorale])

    def testCopitches(self):
        e.copitches(self.chorale, self.chorale[0][0])
        e.copitches(self.chorale, self.chorale[0][4])
        e.copitches(self.chorale, self.chorale[3][6])

    def testCopitchMap(self):
        e.copitch_map(self.chorale)

    def testCountChords(self):
        self.ce.count_chords()
    
    def testChordPairEnergy(self):
        self.chorales = data
        self.ce = e.ChordEnergizer(self.chorales)
        print self.ce.chordCounts
        print self.ce.chordCounts[60]
        self.assertTrue(self.ce.pair_energy({e.pitch_key: 60}, {e.pitch_key: 61}) >
                        self.ce.pair_energy({e.pitch_key: 60}, {e.pitch_key: 63}))

if __name__ == '__main__':
    unittest.main()

