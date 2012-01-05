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
        for i in range(0,len(newJsonDict)-1):
            for j in range(0, len(newJsonDict[i])-1):
                self.assertTrue(newJsonDict[i][j]["pitch"] == jsonDict[i][i]["pitch"])

if __name__ == '__main__':
    unittest.main()
