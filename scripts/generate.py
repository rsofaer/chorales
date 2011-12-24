#!/usr/bin/python

'''
File: generate.py
Author: AFlock
Description: given an input that is a starting pitch and a number of notes, generate a probably note sequence of that duration
'''

import sys
import pickle
import random

def generate(startPitch, duration):
	"""self explanatory"""
	sequence = [startPitch]
	probabilities = pickle.load(open("noteProbs.p", "rb"))
	lastNote = startPitch
	for i in range(duration):
		note = singleGen(lastNote, probabilities)
		sequence.append(note)
		lastNote = note

	print "Sequence is: "
	print sequence
	s = "sequence_%s_%s.p" % (startPitch, duration)
	print "Writing note sequence to ", s
	#dump the new sequence
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
	for i in range(60,76):
		if pr.get(i):
			p[i] = pr.get(i)
		else:
			p[i] = 0
	def func(x):
		if x < p.get(60):
			return 60
		if x < p.get(60) + p.get(61):
			return 61
		if x < p.get(60) + p.get(61) + p.get(62):
			return 62
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63):
			return 63
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64):
			return 64
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65):
			return 65
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66):
			return 66
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67):
			return 67
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68):
			return 68
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68) + p.get(69):
			return 69
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68) + p.get(69) + p.get(70):
			return 70
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68) + p.get(69) + p.get(70) + p.get(71):
			return 71
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68) + p.get(69) + p.get(70) + p.get(71) + p.get(72):
			return 72
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68) + p.get(69) + p.get(70) + p.get(71) + p.get(72) + p.get(73):
			return 73
		if x < p.get(60) + p.get(61) + p.get(62) + p.get(63) + p.get(64) + p.get(65) + p.get(66) + p.get(67) + p.get(68) + p.get(69) + p.get(70) + p.get(71) + p.get(72) + p.get(73) + p.get(74):
			return 74
		return 75
#}}}
	return func


if __name__ == '__main__':
	generate(int(sys.argv[1]), int(sys.argv[2]))


