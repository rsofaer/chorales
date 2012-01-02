'''
File: moreprobs.py
Author: AFlock
Description: records sequence of next two notes based on start note
'''


def main():
    NNcounts = {}
    TNcounts = {}
    #cont that shit
	data = json.load(open("../dataset/chorales.json", "rb"))
    for chorNum, notes in data.iteritems():
        for i in range(len(notes)):
            note = notes[i]
			if i < len(notes) - 2:
				if not nextNextNote.get(note['pitch']):
					nextNextNote[note['pitch']] = {}
                nextNextNote = notes[i+2]
                if NNcounts[note['pitch']].get(nextNextNote['pitch']]):
                    NNcounts[note['pitch']][nextNextNote['pitch']] += 1
                else:
                    NNcounts[note['pitch']][nextNextNote['pitch']] = 1
            #might as well collect for next three
            if i < len(notes) - 3:
               thirdNote = notes[i+2]
                if TNcounts[note['pitch']].get(thirdNote['pitch']]):
                    TNcounts[note['pitch']][thirdNote['pitch']] += 1
                else:
                    TNcounts[note['pitch']][thirdNote['pitch']] = 1


	#then normalize to get a 1-integral distribution
	pitchprob = {}
	for opitch, numbers in NNcounts.iteritems():
		pitchprob[opitch] = {}
		sum = 0
		for p, num in numbers.iteritems():
			sum += num

		for p, num in numbers.iteritems():
			pitchprob[opitch][p] = float(num)/float(sum)

    #then return
    return pitchprob

if __name__ == '__main__':
    probs = main()
    print probs
	pickle.dump(probs, open("nextNoteProbs.p", "wb"))
