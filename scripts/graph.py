#!/usr/bin/python

'''
File: graph.py
Author: AF
Description: created a directed graph of energy-weighted chords
'''

import json

from noteToNoteProbs import probabalize
from chordEnergy import ChordEnergizer

#Global cleandata
cleandata = json.load(open("../dataset/cleandata.json", "rb"))
#chord_list = json.loads(open("../dataset/chord_list", "rb"))

data = cleandata.values()
def hasKeySig(chorale):
    return not chorale[0][0]["keysig"] == None

data = filter(hasKeySig, data)
probs = probabalize(cleandata)
"""
Note: chords here are usually tuples with ([list,of,notes], #energy)
The chords that each Graph object hold look like this:
    {
        ((1,2,3,4), energyOfChord) : {dictionary of "next possible chords/costs"},
        ((3,2,3,4), energyOfChord) : {dictionary of "next possible chords/costs"},
        ((4,2,3,4), energyOfChord) : {dictionary of "next possible chords/costs"}
    }
"""
class Graph():
    """ holds a list of all chord nodes"""
    def __init__(self, duration= 40):
        self.ce = ChordEnergizer(data)
        self.chord_energies = self.ce.chordCounts
        #print self.chord_energies
        self.probs = probs
        self.chords = []
        print len(self.chord_energies)

        for chord, energy in self.chord_energies.iteritems():
            self.chords.append(chordNode(chord, energy,self))

class chordNode():
    """Has a chord, a number of incoming energies and a node energy """
    def __init__(self, chord, energy, graph):
        self.chord = chord
        self.energy = energy
        #outbound is a list of all following chords and the energies to go from one to the next
        self.outbound = []
        """
        This is what crashes:


        for other in graph.chord_energies:
            print "here is the other!"
            print other
            self.outbound.append((other, cross_energy(self.chord, other)))
        """



#most likely this piece is not needed VV
class layer():
    """Holds all possible chords along with weights for each"""
    def __init__(self):
        self.chords = []
        #for chord in chord_list:
            #self.chords.append(chordNode(chord))

def cross_energy(origin, outbound):
    """returns an energy for going from one chord to the other based on note-likelihood for each voice"""
    total_energy = 0
    for i in range(len(origin)):
        voice = {3: "bass", 2: "tenor", 1: "alto", 0: "soprano"}[i]
        print origin
        #TODO how to deal with <4 voices?
        #print probs[voice]
        #print origin
        #print origin[i]
        #print probs[voice][int(origin[i])]
        print "V_V_VV__V__V"
        print "origin :: ", origin
        print "outbound :: ", outbound
        print "i :: ", i
        print probs[voice]
        if len(outbound) > i:
            energy = 1/float(probs[voice][int(origin[i])].get(int(outbound[i]), 0.00000000001))
        else:
            #print i
            #print outbound
            energy = 1/float(probs[voice][int(origin[i])].get(int(outbound[0]), 0.00000000001))
            print energy
        #origin[i] VS outbound[i]
        #get occurence from probabalize (ln 43) add 1/ occ[v][origin[i][outbound[i]]
        total_energy += energy
    return total_energy



if __name__ == '__main__':
    g = Graph(10)
    #print g.generateChorale()
    #print g.whatever_else





