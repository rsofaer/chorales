#!/usr/bin/python

import json
import normalize as normalizer

'''
File: noteToNoteProbs.py
Author: RJS
Description: Given a JSON version of the chorales dataset,
    provide functions for calculating the energy/likelihood of a chord.
'''

pitch_key = "pitch"

class ChordEnergizer:
    def __init__(self, data):
        #self.data = map(normalizer.normalize_chorale(data))
        self.data = data
        pass

    def count_chords(self):
        copitch_map = {}
        for chorale in self.data:
            chorale_copitches = copitch_map(chorale)
            for copitch in note_copitches.keys:
                if not copitch in copitch_map:
                    copitch_map[copitch] = 0
                copitch_map[copitch] += note_copitches[copitch]
    
    def copitch_map(chorale):
        copitch_map = {}
        for note in chorale[0]:
            note_copitches = copitches(chorale, note)
            for copitch in note_copitches.keys:
                if not copitch in copitch_map:
                    copitch_map[copitch] = 0
                copitch_map[copitch] += note_copitches[copitch]

    # Given a note, find the pitches in the chorale that occur at the same time.
    def copitches(chorale, note):
        copitches = {}
        for voice in chorale:
            for conote in voice:
                if ((conote["st"] + conote["dur"]) > note["st"] and conote["st"] < note["st"]) or (conote["st"] > note["st"] and conote["st"] < note["st"] + note["dur"]):
                    if not conote[pitch_key] in copitches:
                        copitches[conote[pitch_key]] = 0
                    copitches[conote[pitch_key]] += 1
        #remove note from copitches
        copitches[note[pitch_key]] -= 1


