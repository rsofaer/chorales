#!/usr/bin/python

import midify
import midiTojson
import unittest

midifile = "../dataset/fourPartChorales/039200b_.mid"
jsontempfile = "round_trip_json_temp"
miditempfile = "round_trip_midi_temp"

class TestMidiJSON(unittest.TestCase):

    def testRoundTrip(self):
        jsonDict = midiTojson.genJson(midifile)
        midify.midify(jsonDict, miditempfile)
        newJsonDict = midiTojson.genJson("../dataset/midi/" + miditempfile + ".mid")
        print jsonDict
        print "_V"*40
        print newJsonDict
        assert(jsonDict == newJsonDict)

if __name__ == '__main__':
    unittest.main()
