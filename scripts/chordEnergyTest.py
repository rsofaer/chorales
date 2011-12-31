#!/usr/bin/python

import chordEnergy as e
import json
import unittest

class TestChordEnergy(unittest.TestCase):

    def setUp(self):
        self.chorale = json.load(open("../dataset/fourPartJSON/007007b_.mid.json", "rb"))
        self.ce = e.ChordEnergizer([self.chorale])

    def testCopitches(self):
        e.copitches(self.chorale, self.chorale[1][0])
        e.copitches(self.chorale, self.chorale[1][4])
        e.copitches(self.chorale, self.chorale[3][6])

    def testCopitchMap(self):
        e.copitch_map(self.chorale)

    def testCountChords(self):
        self.ce.count_chords()

if __name__ == '__main__':
    unittest.main()

