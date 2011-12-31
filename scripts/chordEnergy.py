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
        #self.count_chords()

    def energy(chord):
        melody_note = chord[0]
        total_energy = 0
        for i in range(1, len(chord)):
            total_energy += pair_energy(melody_note, chord[i])
        return total_energy

    def pair_energy(pitch_one, pitch_two):
        pass

    def count_chords(self):
        total_copitch_map = {}
        for chorale in self.data:
            chorale_copitches = copitch_map(chorale)
            for copitch in total_copitch_map.keys():
                if not copitch in total_copitch_map:
                    total_copitch_map[copitch] = 0
                total_copitch_map[copitch] += note_copitches[copitch]
        self.chordCounts = total_copitch_map
    
def copitch_map(chorale):
    copitch_map = {}
    for note in chorale[1]:
        base_pitch = note[pitch_key]
        if not base_pitch in copitch_map:
            copitch_map[base_pitch] = {}
        note_copitches = copitches(chorale, note)
        for copitch in note_copitches.keys():
            if not copitch in copitch_map[base_pitch]:
                copitch_map[base_pitch][copitch] = 0
            copitch_map[base_pitch][copitch] += note_copitches[copitch]
    return copitch_map

# Given a note, find the pitches in the chorale that occur at the same time.
def copitches(chorale, note):
    copitches = {}
    for voice in chorale:
        for conote in voice:
            if (((conote["st"] + conote["dur"]) > note["st"] and conote["st"] <= note["st"]) or 
                 (conote["st"] < note["st"] + note["dur"]) and conote["st"] >= note["st"]):
                if not conote[pitch_key] in copitches:
                    copitches[conote[pitch_key]] = 0
                copitches[conote[pitch_key]] += 1
    #remove note from copitches
    copitches[note[pitch_key]] -= 1
    return copitches


