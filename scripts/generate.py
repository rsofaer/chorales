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
    for i in range(0,15):
        if pr.get(i):
            p[i] = pr.get(i)
        else:
            p[i] = 0
    def func(x):
        #total = 0
        #for x in range(0,20):
        #    total += p.get(x)
        #    if x < total:
        #        return x
        #return false
        if x < p.get(0):
            return 0
        if x < p.get(0) + p.get(1):
            return 1
        if x < p.get(0) + p.get(1) + p.get(2):
            return 2
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3):
            return 3
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4):
            return 4
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5):
            return 5
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6):
            return 6
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7):
            return 7
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8):
            return 8
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9):
            return 9
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10):
            return 10
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11):
            return 11
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12):
            return 12
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13):
            return 13
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13) + p.get(14):
            return 14
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13) + p.get(14) + p.get(15):
            return 15
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13) + p.get(14) + p.get(15)+ p.get(16):
            return 16
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13) + p.get(14) + p.get(15)+ p.get(16)+ p.get(17):
            return 17
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13) + p.get(14) + p.get(15)+ p.get(16)+ p.get(17)+ p.get(18):
            return 18
        if x < p.get(0) + p.get(1) + p.get(2) + p.get(3) + p.get(4) + p.get(5) + p.get(6) + p.get(7) + p.get(8) + p.get(9) + p.get(10) + p.get(11) + p.get(12) + p.get(13) + p.get(14) + p.get(15)+ p.get(16)+ p.get(17)+ p.get(18)+ p.get(19):
            return 19
        return false
    return func
#}}}


if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print "generate.py <start-pitch> <duration>"
        exit()
    generate(int(sys.argv[1]), int(sys.argv[2]))


