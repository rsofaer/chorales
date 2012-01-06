#!/usr/bin/python

'''
File: graph.py
Author: AF
Description: created a directed graph of energy-weighted chords
'''

import json
import sys
from datetime import datetime as dt

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

    SCRAP DAT

    here:

    object layout for:
        graph = [cnode, cnode, cnode]

        cnode{
            self.chord = (1,2,3,4)
            self.energy = .93 (this is the inherent energy for the chord)
            self.outbound = {(some, other, chord, 5) : <number of times that chord happens after this one>, (yet, another, chord): .234, etc}
            self.outbound_cross_e = {(some, other, chord, 5) : <energy for this chord pair from note_to_note>, (yet, another, chord): .234, etc}
            self.outbound_chord_e = {(some, other, chord, 5) : <energy for this chord pair from chordEnergizer>, (yet, another, chord): .234, etc}
        }


"""
class Graph():
    """ holds a list of all chord nodes"""
    def __init__(self, duration= 40):
        time1 = dt.now()

        self.ce = ChordEnergizer(data)
        self.chord_energies = self.ce.chordCounts
        self.chord_changes = self.ce.chordChanges
        self.probs = probs
        self.chords = []
        print "Adding chords"
        i = 0
        for chord, energy in self.chord_energies.iteritems():
            i += 1
            if i%90 == 0:
                sys.stdout.write('.')
            self.chords.append(chordNode(self.ce, chord, energy, self.chord_changes.get(chord, None)))

        time2 = dt.now()
        print ""
        print "total time to load", len(self.chords),  " chords was: ", time2-time1

        for c in chord:
            c.next_chord(self)
            break

class chordNode():
    """Has a chord, a number of incoming energies and a node energy """
    def __init__(self, chord_energizer, chord, energy, outbound):
        self.chord = chord
        print self.chord
        self.energy = energy
        #outbound is a dict of all following chords and the energies to go from one to the next
        assert(outbound)
        self.outbound = outbound
        self.outbound_cross_e = {}
        self.outbound_chord_e = {}
        for other in outbound:
            cross_e = cross_energy(self.chord, other)
            chord_to_chord_energy = chord_energizer.chord_pair_energy(self.chord, other)
            self.outbound_cross_e[other] = cross_energy
            self.outbound_chord_e[other] = chord_to_chord_energy

            
    #instance method, give it a graph,, go through energies and determine the next chord
    def next_chord(self, g):
        print 'SUMMON'
        E1 = float("inf")
        E2 = float("inf")
        E3 = float("inf")
        best_chord = None
        for cn, prob in chord.outbound: #maybe enumerate
            temp1 = prob
            temp2 = cn #look up chord energy in graph
            if temp1 + temp2 < E1 + E2:
                E1 = temp1
                E2 = temp2
                #probably only need one sum
                best_chord = cn
        return best_chord


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
        if not origin[i] or not outbound[i]:
            continue
        if len(outbound) > i:
            energy = 1/float(probs[voice][int(origin[i])].get(int(outbound[i]), 0.00000000001))
        else:
            #print i
            #print outbound
            energy = 1/float(probs[voice][int(origin[i])].get(int(outbound[0]), 0.00000000001))
            #print energy
        #origin[i] VS outbound[i]
        #get occurence from probabalize (ln 43) add 1/ occ[v][origin[i][outbound[i]]
        total_energy += energy
    return total_energy



if __name__ == '__main__':
    g = Graph(10)
    #print g.generateChorale()
    #print g.whatever_else




