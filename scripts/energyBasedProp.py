#!/usr/bin/python

'''
File: energyBasedProp.py
Author: AF
Description: use energies to generate sequences and single
'''

from itertools import product
import operator

"""Constants to scale energy by"""
ALPHA = 0.5 # for the importance of the note-to-note energies
BETA  = 0.5 # for the importance of the chordal energy


def genChord(startChord):
    """
    Uses both energies to generate following chords
            @Input: starting chord [10,22,31,42] a sorted list,
            @Output: following chord(s) [13,20, 29, 44]
    """
    # this will hold all of our chords and their energies
    total_energies = {}

    #for each voice, get a list of probable next notes
    nexts = []
    for i, note in enumerate(startChord):
        nexts.append(generateNoteList(note, 4))

    #now every combination of those along with their combined "energy"
    possible = []
        for combo in a:
            chord = [nexts[0]combo[0][0], nexts[1]combo[1][0], nexts[2]combo[2][0], nexts[3]combo[3][0]]
            energy = (nexts[0]combo[0][1]+ nexts[1]combo[1][1]+ nexts[2]combo[2][1]+ nexts[3]combo[3][1])
            possible.append((chord, energy))


    #now figure out the liklihood for all of these chords
    for chord, energy in possible:
        total_energies[chord] = (ALPHA * energy) + (BETA * energy(chord))

    #now choose the lowest energy chord

    chosen  = sorted(total_energies.iteritems(), key=operator.itemgetter(1))[0][0]

    return chosen



if __name__ == '__main__':
    print genChord[10,20,30,40]




