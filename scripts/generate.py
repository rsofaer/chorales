#!/usr/bin/python

'''
File: generate.py
Author: AFlock
Description: given an input that is a starting pitch and a number of notes, generate a probably note sequence of that duration
'''

import sys
import pickle
import random
import midify
import normalize

def generate(startPitch, duration):
    """self explanatory"""
    sequence = []
    probabilities = pickle.load(open("noteProbs.p", "rb"))
    lastNote = startPitch
     #{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0},
    #lets just say the keysig is -1 for now

    for i in range(duration):
        time = (i+1)*4
        note = singleGen(lastNote, probabilities)
        toAdd = {"st" : time , "pitch": note, "dur":4, "keysig":-1, "timesig": 12, "fermata" :0 }
        toAdd ["pitch"] = normalize.denormalize_pitch(toAdd)
        sequence.append(toAdd)
        lastNote = note

    print "Sequence is: "
    print sequence

    s = "sequence_%s_%s.p" % (startPitch, duration)
    #print "Writing note sequence to ", s

    #midify the new sequence
    midify.midify(sequence, "genoutput%s%s" % (startPitch, duration))
    #pickle.dump(sequence, open(s, "wb"))


def singleGen(note, probs):
    """returns a probable next note"""
    #first, choose a random number.
    rand = random.random()
    #then choose from the distribution
    individualProbs = probs[note]
    distr = distribution(individualProbs)
    result = distr(rand)
    return result


def distribution(pr):
    "returns a distribution function"#{{{
    p = {}
    #sanitize for nonetypes
    for i in range(0,19):
        if pr.get(i):
            p[i] = pr.get(i)
        else:
            p[i] = 0
    def func(x):
        #much cleaner
        total = 0
        for i in range(0,20):
            total += p.get(i)
            if x < total:
                return i
        return false
    return func
#}}}


if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print "generate.py <start-pitch> <duration>"
        exit()
    generate(int(sys.argv[1]), int(sys.argv[2]))


