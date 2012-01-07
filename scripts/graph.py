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
import chordEnergy as che
from midify import midify


#Global cleandata
cleandata = json.load(open("../dataset/cleandata.json", "rb"))

def hasKeySig(chorale):
    return not chorale[0][0]["keysig"] == None

#Global list of cleandata.values with a keysig
data = cleandata.values()
data = filter(hasKeySig, data)

def tableify(l):
    l_out = []
    for i in range(len(l[0])):
        l_out.append([v[i] for v in l])
    return l_out


def record_prog_stats(data):

    progressions = {} #ending progressions
    for chorale in data:
        table = che.table_from_chorale(chorale)
        table = tableify(table)
        last_prog= tuple([tuple(i) for i in table[-16:]])
        progressions[last_prog] = progressions.get(last_prog, 0) + 1

    #print progressions.values()
    return progressions

#last_chord must be cnode to get graph!
def end_chorale(last_chord):
    #print ending_progressions
    best_e = float("inf")
    best_ch = None #..yet!
    for key, value in ending_progressions.iteritems():
        temp_e = get_energy(tuple([last_chord.chord])+key, last_chord.graph)
        if temp_e < best_e:
            best_e = temp_e
            best_ch = key
    #print best_e
    return best_ch

def get_energy(ll,g):
    alpha = 0.0000001
    beta = 4.0
    gamma = 10.5
    delta = 0.0000001
    
    total_e = 0

    ##SOMETIMES THERE ARE CHORDS IN HERE THAT ARE NOT IN G.CHORDS
    ##CANT EXPLAIN THAT (ALIENS)
    l = [g.chords[x] if x in g.chords else "FUCK" for x in ll]
    if "FUCK" in l:
        #print "FUCK'D"
        return float("inf")


    #first cnode is the last chord of the generated chorale
    #delta = 0.0 #how much to weigh the occurrences
    for index, chord in enumerate(l):

        #current chord's energy
        total_e += alpha*chord.energy
        #cross entropy
        if(index+1 < len(l)):
            total_e += beta*chord.outbound_cross_e[l[index+1].chord] if l[index+1].chord in chord.outbound_cross_e else float("inf")
        #next chord energy
        if(index+1 < len(l)):
            total_e += gamma*chord.outbound_chord_e[l[index+1].chord] if l[index+1].chord in chord.outbound_chord_e else float("inf")
        
    total_e += delta*1.0/ending_progressions[ll[1:]]
    #print total_e
    return total_e

ending_progressions = record_prog_stats(data)
probs = probabalize(cleandata)

"""
    object layout for:
        graph = {chord : cnode, chord : cnode, chord : cnode}

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

        self.ce = che.ChordEnergizer(data)
        self.chord_energies = self.ce.chordCounts #slightly misleading- gets turned from count to energy in ln 57
        self.chord_changes = self.ce.chordChanges
        self.probs = probs
        self.chords = {}
        print "Adding chords"
        i = 0
        for chord, count in self.chord_energies.iteritems():
            i += 1
            if i%90 == 0:
                sys.stdout.write('.')
            #how can we do his every time ? VV
            energy = self.ce.chord_energy(chord, normed=True)
            self.chords[chord] = chordNode(self, self.ce, chord, energy, self.chord_changes.get(chord, None))

        time2 = dt.now()
        print ""
        print "total time to load", len(self.chords),  " chords was: ", time2-time1

class chordNode():
    """Has a chord, a number of incoming energies and a node energy """
    def __init__(self, graph, chord_energizer, chord, energy, outbound):
        self.graph = graph
        self.chord = chord
        self.energy = energy
        #outbound is a dict of all following chords and the energies to go from one to the next
        assert(outbound)
        self.outbound = outbound
        self.outbound_cross_e = {}
        self.outbound_chord_e = {}
        for other in outbound:
            cross_e = cross_energy(self.chord, other)
            chord_to_chord_energy = chord_energizer.chord_pair_energy(self.chord, other)
            self.outbound_cross_e[other] = cross_e
            self.outbound_chord_e[other] = chord_to_chord_energy


    #instance method, give it a graph,, go through energies and determine the next chord
    def next_chord(self):

        #Weights: alpha|E1, beta|E2, gamma|E3
        alpha = 0.0000001
        beta = 4.0
        gamma = 10.5
        delta = 0.0000001

        #Energies: E1|cnode.energy, E2|cnode.outbound_cross_e, E3|outbound_chord_e
        E1 = float("inf")
        E2 = float("inf")
        E3 = float("inf")

        best_chord = None # ...yet!

        for ch in self.outbound:

            temp1 = self.graph.chords[ch].energy #the energy of the chord
            temp2 = self.outbound_cross_e[ch]
            temp3 = self.outbound_chord_e[ch]

            if temp1*alpha + temp2*beta + temp3*gamma < E1*alpha + E2*beta + E3*gamma:
                E1 = temp1
                E2 = temp2
                E3 = temp3
                best_chord = self.graph.chords[ch]


        #make that chord less likely
        self.graph.ce.chordCounts[best_chord.chord] *= delta
        #also want to re-energize that chord
        #print "before: ", best_chord.energy
        best_chord.energy = self.graph.ce.chord_energy(best_chord.chord, normed=True)
        #print "after: ", best_chord.energy

        return best_chord


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
            energy = 1/float(probs[voice][int(origin[i])].get(int(outbound[0]), 0.00000000001))
        total_energy += energy
    return total_energy


def testGeneration():
    """take a midi of an original chorale, table-fy it, take first chord, generate a new table from our energies, compare"""
    #will return a loss for the specific values of alpha beta gamma (sorority?)
    print "starting the test"
    #midifile = "../dataset/fourPartChorales/039200b_.mid"
    #json_dict = midiTojson.genJson(midifile)

    #for chorale in data:
        #json_dict = chorale
        #break

    json_dict = data[5]
    #tableify
    test_table = che.table_from_chorale(json_dict)
    g = Graph()

    """
    endTime = che.chorale_end_time(json_dict)
    for time in range(0,endTime-1):
        chordList = map(lambda v: v[time], test_table)
        first_chord = tuple(chordList)
        break
    """

    #first_chord = test_table[0]
    #print first_chord
    #first_chord = g.chords.get(tuple(first_chord))

    print "generate!"
    #flip test_table
    test_table = tableify(test_table)
    first_chord = g.chords.get(tuple(test_table[0]))
    assert (first_chord)
    generated_sequence = generate(first_chord, 50)


    #write that to a midi
    chords_to_midi(generated_sequence)



    total_loss = 0

    for i in range(50):
        total_loss += lossify(test_table[i], generated_sequence[i].chord)

    print "total loss is: ", total_loss

def chords_to_midi(chords):
    """takes a chord sequence from generate and jsons then midis it"""
    #first need to put it in json format (4 voices)
    json_dict = [[],[],[],[]]
    note_template = {'timesig': None, 'keysig': 0, 'tempo': 90, 'st': 0, 'pitch': None, 'dur': 0, 'fermata': 0}

    chords = map(lambda c: denormalize_chord(c.chord), chords)

    for voice in range(len(chords[0])):
        cur_note = note_template.copy()
        cur_note['pitch'] = chords[0][voice]
        for time in range(0, len(chords)):
            if chords[time][voice] == cur_note['pitch']:
               cur_note['dur'] += 4
            else:
               json_dict[voice].append(cur_note)
               cur_note = note_template.copy()
               cur_note['st'] = time*4
               cur_note['pitch'] = chords[time][voice]
               cur_note['dur'] = 4
        json_dict[voice].append(cur_note)

    midify(json_dict)


def lossify(c1, c2):
    """loss per two chords on simple euclidean distance"""

    total = 0
    for i in range(len(c1)):
        total +=(abs(c1[i] - c2[i]) if c1[i] != None and c2[i] != None else 0)
        if (c2[i] == None and c2[i] != None) or (c1[i] != None and c2[i] == None):
            total += 19

    return total

#returns the list of generated chords
def generate(chord, length):
    #assuming chord is a cnode!!
    l = [chord]
    #Minus 1 because we have a starting chord
    #Minus 16 to append the ending
    for i in range(length-1-16):
        l.append(l[-1].next_chord())
    
    #Append ending

    #example of bitch that doesn't work
    #print (4, None, None, None) in g.chords #False
    #print (4, None, None, None) in g.chord_changes #TRUE?! Aliens.


    end = end_chorale(l[-1])

    print "End Chorale:\n", end
    
    l.extend([chord.graph.chords[x] for x in end])

    return l


def denormalize_chord(chord):
    """ Takes a tuple representing a chord, returns a new tuple"""
    newChord = list(chord)
    offsets = [60,48,48,36]
    for i in range(0, len(newChord)):
        if type(newChord[i]) == int:
            newChord[i] += offsets[i]

    return tuple(newChord)



if __name__ == '__main__':
    time1 = dt.now()
    """
    g = Graph(10)

    #Testing next_chord()
    num = 100
    ch = 0
    for c in g.chords:
        ch = c
        break
    for i in range(num):
        print "The best chord to follow",c,"is",g.chords[c].next_chord().chord
        chor = g.chords[c].next_chord()
        c = chor.chord

    """

    
    testGeneration()
    time2 = dt.now()
    print "total time : ", time2-time1




