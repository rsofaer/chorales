#!/usr/bin/python

import chordEnergy as e
import json
import unittest

class TestChordEnergy(unittest.TestCase):

    def setUp(self):
        self.chorale = json.load(open("../dataset/fourPartJSON/007007b_.mid.json", "rb"))
        self.ce = e.ChordEnergizer([self.chorale])

    def testCopitches(self):
        e.ChordEnergizer.copitches(self.chorale, self.chorale[0][0])
        e.ChordEnergizer.copitches(self.chorale, self.chorale[0][4])
        e.ChordEnergizer.copitches(self.chorale, self.chorale[3][6])

    def testCopitchMap(self):
        e.ChordEnergizer.copitch_map(self.chorale)

    def testCountChords(self):
        self.ce.count_chords()

if __name__ == '__main__':
    unittest.main()

