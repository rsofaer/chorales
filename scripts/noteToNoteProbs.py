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
    counts = {"bass": {}, "tenor": {}, "soprano": {}, "alto": {} }
    """
    counts = {"bass": {sub}, "tenor": {sub}, "soprano": {sub}, "alto": {sub} }

    subcounts = {69: {65: 1, 64: 2, ... }}
    """

    for name, chorale in data.iteritems():
        print name
        voices = {}
        avgNums = []

        #lets find which voice is which part by finding their relative average pitches
        for voice in chorale:
            if len(voice)<1:
                continue
            total = 0
            for i, note in enumerate(voice):
                total += note["pitch"]
            avgPitch = float(total)/float(i+1)
            voices[avgPitch] = voice
            avgNums.append(avgPitch)

        avgNums.sort()
        if len(avgNums) is not 4:
            continue
        for j, number in enumerate(avgNums):
            if j is 0:
                name = "bass"
            if j is 1:
                name = "tenor"
            if j is 2:
                name = "soprano"
            if j is 3:
                name = "alto"

            theVoice = voices[number]

            #for each note, what is the next note?
            for h, note in enumerate(theVoice):
                if h < len(theVoice) - 1:
                    nextNote = theVoice[h+1]
                    #note = normalize.normalize_pitch(note)
                    #nextNote = normalize.normalize_pitch(nextNote)
                    note = note["pitch"]
                    nextNote = nextNote["pitch"]

                    if not counts[name].get(note):
                        counts[name][note] = {}

                    #I love python
                    counts[name][note][nextNote] = counts[name][note].get(nextNote, 0) + 1


    return counts

"""
OLD WHEY

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

"""

if __name__ == '__main__':
    #get Data
    #normalize?
    #run that shit
    #pickle the result

    ##data = {194: [{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}, {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}] }
    #data = {"one" : [[{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}, {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}], [{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}, {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}], [{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}, {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}], [{"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}, {"st": 12  ,  "pitch": 69,  "dur": 8 ,  "keysig": -1,  "timesig": 12,  "fermata": 0}]]}
    data = json.load(open("../dataset/fourPartJSON.json", "rb"))
    probs = probabalize(data)

    print probs
    #pickle.dump(probs, open("noteProbs.p", "wb"))
