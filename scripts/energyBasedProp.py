#!/usr/bin/python

'''
File: energyBasedProp.py
Author: AF
Description: use energies to generate sequences and single
'''

from generate import generateNoteList
from itertools import product
import chordEnergy as ce

import json
import operator

"""Constants to scale energy by"""
ALPHA = 0.5 # for the importance of the note-to-note energies
BETA  = 0.5 # for the importance of the chordal energy

def hasKeySig(chorale):
    return not chorale[0][0]["keysig"] == None


def genChord(startChord):
    """
    Uses both energies to generate following chords
            @Input: starting chord [10,22,31,42] a sorted list,
            @Output: following chord(s) [13,20, 29, 44]
    """
    # this will hold all of our chords and their energies
    total_energies = {}

    #get a chord energizer
    data = json.load(open("../dataset/cleandata.json", "rb")).values()
    data = filter(hasKeySig, data)
    c = ce.ChordEnergizer(data)

    #for each voice, get a list of probable next notes
    nexts = []
    for i, note in enumerate(startChord):
        voice = {0: "bass", 1: "tenor", 2: "alto", 3: "soprano"}[i]
        nexts.append(generateNoteList(voice, note, 4))

    #now every combination of those along with their combined "energy"
    possible = []

    p = product([0,1,2,3], repeat = 4)

    for combo in p:
        print combo
        chord = [nexts[0][combo[0]][0], nexts[1][combo[1]][0], nexts[2][combo[2]][0], nexts[3][combo[3]][0]]
        energy = (nexts[0][combo[0]][1]+ nexts[1][combo[1]][1]+ nexts[2][combo[2]][1]+ nexts[3][combo[3]][1])
        possible.append((chord, energy))


    #now figure out the liklihood for all of these chords
    for chord, energy in possible:
        print str(chord) + ":::" + str(energy)
        total_energies[tuple(chord)] = (ALPHA * energy) + (BETA * c.energy(chord))

    #now choose the lowest energy chord

    chosen  = sorted(total_energies.iteritems(), key=operator.itemgetter(1))[0]

    return chosen



if __name__ == '__main__':
    print genChord([0,4,3,1])




