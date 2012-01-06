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
        self.count_intervals()
        self.count_chords()

    def sum_pair_energy(self, chord):
        if not type(chord[0]) is int and 'pitch' in chord[0]:
            norm_chord = normalizer.normalize_sequence(chord)
        else:
            norm_chord = chord
        melody_note = norm_chord[0]
        total_energy = 0
        for i in range(1, len(chord)):
            total_energy += self.pair_energy(melody_note, norm_chord[i])
        return total_energy

    # This energy function does not use pairEnergy and intervalCounts
    # It uses chordCounts.
    def chord_energy(self, chord):
        if not type(chord[0]) is int and 'pitch' in chord[0]:
            norm_chord = normalizer.normalize_sequence(chord)
        else:
            norm_chord = chord
        chordString = chordStringFromList(norm_chord)

        if not chordString in self.chordCounts:
            return 999999999.0
        return 1.0/self.chordCounts[chordString]

    def pair_energy(self, pitch_one, pitch_two):
        if type(pitch_one) is int:
            pitch_one_i = pitch_one
            pitch_two_i = pitch_two
        else:
            pitch_one_i = pitch_one[pitch_key]
            pitch_two_i = pitch_two[pitch_key]
        copitches = self.intervalCounts[pitch_one_i]
        if not pitch_two_i in copitches:
            return 99999999.0
        return 1.0/self.intervalCounts[pitch_one_i][pitch_two_i]

    def count_intervals(self):
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
        self.intervalCounts = total_copitch_map

    def count_chords(self):
        chord_counts = {}
        for chorale in self.data:
            add_hash(chord_counts, chorale_chords(chorale))
        self.chordCounts = chord_counts

def chorale_chords(chorale):
    chord_counts = {}
    endTime = chorale_end_time(chorale)
    table = table_from_chorale(chorale)
    for time in range(0,endTime-1):
        chordList = map(lambda v: v[time], table)
        chord_string = chordStringFromList(chordList)
        if not chord_string in chord_counts:
            chord_counts[chord_string] = 0
        chord_counts[chord_string] += 1
    
    return chord_counts

def table_from_chorale(chorale):
    table = []
    end_time = chorale_end_time(chorale)
    base_list = map(lambda i: None, range(0,end_time))
    for voice in chorale:
        voice_row = list(base_list)
        noteCounter = 0
        for time in range(0, end_time):
            if noteActiveAt(voice[noteCounter], time):
                voice_row[time] = voice[noteCounter][pitch_key]
            else:
                if not voice[noteCounter]["st"] > time:
                    noteCounter += 1
                    if noteCounter >= len(voice):
                        break
                if noteActiveAt(voice[noteCounter], time):
                    voice_row[time] = voice[noteCounter][pitch_key]
        table.append(voice_row)
    return table
        

def chorale_end_time(chorale):
    last_notes = map(lambda v: v[len(v)-1], chorale)
    end_times = map(lambda n: int(n["st"] + n["dur"]), last_notes)
    return max(end_times)

def chordStringFromList(chordList):
    if type(chordList[0]) == dict:
        chordList = map(lambda d: d[pitch_key], chordList)
    chordString = ""
    for x in chordList:
        chordString += str(x) + ","

    return chordString

def noteActiveAt(note, time):
    return note["st"] <= time and note["st"] + note["dur"] >= time

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
