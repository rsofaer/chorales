#!/usr/bin/python

import midify
import midiTojson
import unittest

midifile = "../dataset/fourPartChorales/00101b_.mid"
jsontempfile = "round_trip_json_temp"
miditempfile = "round_trip_midi_temp"

class TestMidiJSON(unittest.TestCase):
    
    def testRoundTrip(self):
        jsonDict = midiTojson.genJson(midifile)
        midify.midify(jsonDict, miditempfile)
        newJsonDict = midiTojson.genJson(miditempfile)
        print jsonDict
        print
        print newJsonDict
        assertTrue(jsonDict == newJsonDict)

