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
        self.tables = map(table_from_chorale, data)
        self.count_intervals()
        self.count_chords()
        self.count_chord_changes()

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
    def chord_energy(self, chord, normed=False):
        norm_chord = None
        if not normed:
            if not type(chord[0]) is int and 'pitch' in chord[0]:
                norm_chord = normalizer.normalize_sequence(chord)
            else:
                norm_chord = chord
        else:
            norm_chord = chord

        if type(norm_chord[0]) == dict:
            norm_chord = map(lambda n: n[pitch_key], norm_chord)

        chord_tuple = tuple(norm_chord)

        if not chord_tuple in self.chordCounts or self.chordCounts[chord_tuple] == 0:
            return 999999999
        return 1.0/self.chordCounts[chord_tuple]

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

    def chord_pair_energy(self, chord_one, chord_two):
        if type(chord_one[0]) == dict:
            f = lambda n: n[pitch_key]
            chord_one = map(f, chord_one)
            chord_two = map(f, chord_two)
        chord_one = tuple(chord_one)
        chord_two = tuple(chord_two)

        if chord_one == chord_two:
            return 999999.0
        if not chord_one in self.chordChanges:
            return 999999999.0
        if not chord_two in self.chordChanges[chord_one]:
            return 9999999.0
        return 1.0/self.chordChanges[chord_one][chord_two]



    def count_intervals(self):
        total_copitch_map = {}
        for chorale_table in self.tables:
            chorale_copitches = copitch_map(chorale_table)
            for copitch in chorale_copitches.keys():
                if not copitch in total_copitch_map:
                    total_copitch_map[copitch] = {}
                add_hash(total_copitch_map[copitch], chorale_copitches[copitch])
        self.intervalCounts = total_copitch_map

    def count_chord_changes(self):
        total_chord_change_map = {}
        previous_moment = None
        for table in self.tables:
            for time in range(0, len(table[0])):
                moment = tuple(map(lambda v: v[time], table))
                if not previous_moment in total_chord_change_map:
                    total_chord_change_map[previous_moment] = {}
                if not moment in total_chord_change_map[previous_moment]:
                    total_chord_change_map[previous_moment][moment] = 0
                total_chord_change_map[previous_moment][moment] += 1
                previous_moment = moment
        self.chordChanges = total_chord_change_map

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
        chord_tuple = tuple(chordList)
        if not chord_tuple in chord_counts:
            chord_counts[chord_tuple ] = 0
        chord_counts[chord_tuple] += 1
    return chord_counts

def table_from_chorale(chorale):
    table = []
    end_time = chorale_end_time(chorale)
    base_list = map(lambda i: None, range(0,end_time))
    for voice in chorale:
        voice_row = list(base_list)
        noteCounter = 0
        for time in range(0, end_time):
            if not voice[noteCounter].get('norm_pitch'):
                voice[noteCounter] = normalizer.normalize(voice[noteCounter])
            if noteActiveAt(voice[noteCounter], time):
                voice_row[time] = voice[noteCounter][pitch_key]
            else:
                if not voice[noteCounter]["st"] > time:
                    noteCounter += 1
                    if noteCounter >= len(voice):
                        break
                if not voice[noteCounter].get('norm_pitch'):
                    voice[noteCounter] = normalizer.normalize(voice[noteCounter])
                if noteActiveAt(voice[noteCounter], time):
                    voice_row[time] = voice[noteCounter][pitch_key]
        table.append(voice_row)
    #print table
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

def copitch_map(chorale_table):
    copitch_map = {}
    previous_moment = None
    for time in range(0, len(chorale_table[0])):
        moment = tuple( map(lambda v: v[time], chorale_table))
        if not previous_moment == moment:
            base_pitch = moment[0]
            if not base_pitch in copitch_map:
                copitch_map[base_pitch] = {}
            for i in range(1, len(chorale_table)):
                copitch = moment[i]
                if not copitch in copitch_map[base_pitch]:
                    copitch_map[base_pitch][copitch] = 0
                copitch_map[base_pitch][copitch] += 1
        previous_moment = moment
    return copitch_map

def add_hash(hash_one, hash_two):
    for k in hash_two.keys():
        if not k in hash_one:
            hash_one[k] = 0
        hash_one[k] += hash_two[k]

