#!/usr/bin/python

'''
File: graph.py
Author: AF
Description: created a directed graph of energy-weighted chords
'''

import json

from noteToNoteProbs import probabalize

#Global of all chords
chord_list = json.loads(open("../dataset/chord_list", "rb"))


"""
Note: chords here are usually tuples with ([list,of,notes], #energy)

"""
class chordNode():
    """Has a chord, a number of incoming energies and a node energy """
    def __init__(chord):
        self.chord = chord[0]
        self.energy = chord[1]
        #outbound is a list of all following chords and the energies to go from one to the next
        self.outboud = []
        for other in chord_list:
            self.outbound.append((other, cross_energy(self.chord, other)))


class layer():
    """Holds all possible chords along with weights for each"""
    def __init__():
        self.chords = []
        for chord in chord_list:
            self.chords.append(chordNode(chord))


class graph():
    """ holds layers"""
    def __init__(duration= 40)
    data = json.load(open("../dataset/cleandata.json", "rb"))
    self.probs = probabalize(data)
    self.layers = []
    for i in range(duration):
        self.layers.append(layer())

def genGraph():
    """creates a directed graph of possible chord progression with energies a"""



def cross_energy(origin, outbound):
    """returns an energy for going from one chord to the other based on note-likelihood for each voice"""
    total_energy = 0
    for i in range(4):
        voice = {3: "bass", 2: "tenor", 1: "alto", 0: "soprano"}[i]
        #origin[i] VS outbound[i]
        #get occurence from probabalize (ln 43) add 1/ occ[v][origin[i][outbound[i]]
        total_energy += energy
    return total_energy









