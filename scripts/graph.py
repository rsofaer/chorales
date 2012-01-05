#!/usr/bin/python

'''
File: graph.py
Author: AF
Description: created a directed graph of energy-weighted chords
'''

import json

from noteToNoteProbs import probabalize

#Global cleandata
cleandata = json.load(open("../dataset/cleandata.json", "rb"))
#chord_list = json.loads(open("../dataset/chord_list", "rb"))



"""
Note: chords here are usually tuples with ([list,of,notes], #energy)

"""
class chordNode():
    """Has a chord, a number of incoming energies and a node energy """
    def __init__(self, chord):
        self.chord = chord[0]
        self.energy = chord[1]
        #outbound is a list of all following chords and the energies to go from one to the next
        self.outboud = []
        for other in chord_list:
            self.outbound.append((other, cross_energy(self.chord, other)))


class layer():
    """Holds all possible chords along with weights for each"""
    def __init__(self):
        self.chords = []
        for chord in chord_list:
            self.chords.append(chordNode(chord))


class Graph():
    """ holds layers"""
    def __init__(self, duration= 40):
        self.chord_e = ChordEnergy(cleandata)
        self.probs = probabalize(data)
        self.layers = []
        for i in range(duration):
            self.layers.append(layer())


def cross_energy(origin, outbound):
    """returns an energy for going from one chord to the other based on note-likelihood for each voice"""
    total_energy = 0
    for i in range(4):
        voice = {3: "bass", 2: "tenor", 1: "alto", 0: "soprano"}[i]
        #origin[i] VS outbound[i]
        #get occurence from probabalize (ln 43) add 1/ occ[v][origin[i][outbound[i]]
        total_energy += energy
    return total_energy



if __name__ == '__main__':
    g = Graph(10)
    print g.generateChorale()
    #print g.whatever_else





