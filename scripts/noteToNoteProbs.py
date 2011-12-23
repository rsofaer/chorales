#!/usr/bin/python

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
	for chorNum, notes in data.iteritems():
		for i in range(len(notes)):
			if notes[i+1]:
				note = notes[i]
				nextNote = notes[i+1]
				counts[note['pitch']][nextNote['pitch']] += 1

	#then normalize to get a 1-integral distribution
	pitchprob = {}
	for opitch, numbers in counts.iteritems():
		sum = 0
		for p, num in numbers.iteritems():
			sum += num
		for p, num in numbers.iteritems():
			pitchprob[opitch][p] = num/sum


	return pitchprobs

if __name__ == '__main__':
	#get Data
	#normalize?
	#run that shit
	#pickle the result

	probs = probabalize(data)

	pickle.dump(probs, open("noteProbs.p", "wb"))

