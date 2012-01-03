#!/usr/bin/python

import sys
import json
import normalize as normalizer

'''
File: noteToNoteProbs.py
Author: RJS
Description: Given a JSON version of the chorales dataset,
    provide functions for calculating the energy/likelihood of a chord.
'''

pitch_key = "norm_pitch"

class ChordEnergizer:
    def __init__(self, data):
        self.data = map(normalizer.normalize_chorale,data)
        self.count_chords()

    def energy(self, chord):
        norm_chord = normalizer.normalize_sequence(chord)
        melody_note = norm_chord[0]
        total_energy = 0
        for i in range(1, len(chord)):
            total_energy += pair_energy(melody_note, norm_chord[i])
        return total_energy

    def pair_energy(self, pitch_one, pitch_two):
        copitches = self.chordCounts[pitch_one[pitch_key]]
        if not pitch_two[pitch_key] in copitches:
            return 99999999
        return 1.0/self.chordCounts[pitch_one[pitch_key]][pitch_two[pitch_key]]

    def count_chords(self):
        total_copitch_map = {}
        count = 0
        sys.stderr.write("ChordEnergy processing chorales: ")
        for chorale in self.data:
            sys.stderr.write(".")
            count+=1
            chorale_copitches = copitch_map(chorale)
            for copitch in chorale_copitches.keys():
                if not copitch in total_copitch_map:
                    total_copitch_map[copitch] = {}
                add_hash(total_copitch_map[copitch], chorale_copitches[copitch])
        sys.stderr.write("\n")
        self.chordCounts = total_copitch_map
    
def copitch_map(chorale):
    copitch_map = {}
    for note in chorale[0]:
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

def add_hash(hash_one, hash_two):
    for k in hash_two.keys():
        if not k in hash_one:
            hash_one[k] = 0
        hash_one[k] += hash_two[k]
