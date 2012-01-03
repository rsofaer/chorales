#!/usr/bin/python

'''
File: generate.py
Author: AFlock
Description: given an input that is a starting pitch and a number of notes, generate a probably note sequence of that duration
'''

import sys
import pickle
import random
import operator
import json


#our imports
import normalize
import midify
from noteToNoteProbs import probabalize

#Global probabilites
#probabilities = pickle.load(open("noteProbs.p", "rb"))
#get prob distribution
data = json.load(open("../dataset/cleandata.json", "rb"))
probabilities = probabalize(data)
#TODO raw_distr (run noteToNoteProbs.py)

def generate(startPitch, duration):
    """generate a sequence of notes note: doesn't quite work since we need to incorporate voice'"""
    sequence = []
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
    for note in sequence:
        print note

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

def generateNoteList(voice, note, x):
    """
    Returns a list of the X most likely next notes paired with their occurence in a tuple
    needs a voice to generate on
    [(note, occurence), (note, occurence), (etc)]
    """

    p = {}

    #get prob distribution
    #data = json.load(open("../dataset/cleandata.json", "rb"))
    #probabilities = probabalize(data)

    print probabilities.get(voice).get(note)
    #sanitize for nonetypes
    #this is assuming normalization to range 0-19 has been done
    for i in range(0,19):
        if probabilities.get(voice).get(note).get(i):
            p[i] = probabilities.get(voice).get(note).get(i)
        else:
            p[i] = 0
    prob_list = sorted(p.iteritems(), key=operator.itemgetter(1))
    #turn it into actual probs
    for i in range(len(prob_list)):
        if prob_list[i][1] is 0:
            prob_list[i] = (prob_list[i][0], 100000000)
        prob_list[i] = (prob_list[i][0], 1/float(prob_list[i][1]))

    #print prob_list[-x:]
    return prob_list[-x:]


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
            total += p.get(i, 0)
            if x < total:
                return i
        return false
    return func
#}}}


if __name__ == '__main__':
    if(len(sys.argv) < 3):
        print "generate.py <start-pitch> <duration>"
        exit()
    #generate(int(sys.argv[1]), int(sys.argv[2]))
    print generateNoteList("tenor", int(sys.argv[1]), 4)



