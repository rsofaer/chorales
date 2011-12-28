#!/usr/bin/python

import normalize
import pickle
import json

'''
File: noteToNoteProbs.py
Author: AFlock
Description: Given a JSON version of the chorales dataset,
    output a dictionary of probability distributions for the next note.
'''

def probabalize(data):
    """
     {"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0},
     {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0},
    """
    counts = {}
    """
    counts = {69: {65: 1, 64: 2, ... }}
    """
    #first count all the occurences in our data set
    # we are tracking

    #for each chorale
    for chorNum, notes in data.iteritems():
        #for each note in the chorale
        for i in range(len(notes)):
            if i < len(notes) - 1:
                note = notes[i]
                nextNote = notes[i+1]
                #normalize
                note = normalize.normalize_pitch(note)
                nextNote = normalize.normalize_pitch(nextNote)
                if not counts.get(note):
                    counts[note] = {}
                if counts[note].get(nextNote):
                    counts[note][nextNote] += 1
                else:
                    counts[note][nextNote] = 1

    #then normalize to get a 1-integral distribution
    pitchprob = {}
    for opitch, numbers in counts.iteritems():
        pitchprob[opitch] = {}
        sum = 0
        for p, num in numbers.iteritems():
            sum += num

        for p, num in numbers.iteritems():
            pitchprob[opitch][p] = float(num)/float(sum)


    return pitchprob

if __name__ == '__main__':
    #get Data
    #normalize?
    #run that shit
    #pickle the result

    #data = {194: [{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}, {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}] }
    data = json.load(open("../dataset/chorales.json", "rb"))
    probs = probabalize(data)

    print probs
    pickle.dump(probs, open("noteProbs.p", "wb"))
