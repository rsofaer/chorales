#!/usr/bin/python

import midify
import midiTojson
import unittest

midifile = "../dataset/fourPartChorales/039200b_.mid"
jsontempfile = "round_trip_json_temp"
miditempfile = "round_trip_midi_temp"
miditempfile2 = "round_trip_midi_temp2"

class TestMidiJSON(unittest.TestCase):

    def testRoundTrip(self):
        jsonDict = midiTojson.genJson(midifile)
        midify.midify(jsonDict, miditempfile)
        newJsonDict = midiTojson.genJson("../dataset/midi/" + miditempfile + ".mid")
        #remidify
        midify.midify(newJsonDict, miditempfile2)
        print jsonDict
        print "_V"*40
        print newJsonDict
        for i in range(0,len(newJsonDict)-1):
            for j in range(0, len(newJsonDict[i])-1):
                if not newJsonDict[i][j]["pitch"] == jsonDict[i][j]["pitch"]:
                    print "i :: ", i
                    print "j :: ", j
                    print newJsonDict[i][j]
                    print jsonDict[i][j]
                if not newJsonDict[i][j]["dur"] == jsonDict[i][j]["dur"]:
                    print "i :: ", i
                    print "j :: ", j
                    print newJsonDict[i][j]
                    print jsonDict[i][j]
                self.assertEqual(newJsonDict[i][j]["pitch"], jsonDict[i][j]["pitch"])
                self.assertEqual(newJsonDict[i][j]["dur"], jsonDict[i][j]["dur"])

if __name__ == '__main__':
    unittest.main()
