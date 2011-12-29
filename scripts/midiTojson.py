import sys
import json
import mingus
import mingus.midi.MidiFileIn as mi

'''
File: midiTojson.py
Author: AFlock
Description: turns a midi to a json like we're used to. Requires mingus
'''
def main(file):
    try:
        composition = mi.MIDI_to_Composition(file)
    except Error as e:
        print e

    #print composition
    tempo = composition[1]

    print tempo
    compositionList = []
    for voice in composition[0]:
        noteSequence = []
        st = 0
        for bar in voice:
            for note in bar:
                dur = 16/note[1]
                pitch = note[2]
                if len(pitch) < 1:
                    continue
                pitch = pitch[0]
                pitchNum = int(pitch)
                noteDict = {"st":st, "pitch" : pitchNum, "dur" : dur, "keysig": '?', "timesig" : 12, "fermata": '?'}
                noteSequence.append(noteDict)
                st += dur
        compositionList.append(noteSequence)


    fname = "../dataset/fourPartJSON/" + file.split("/")[-1] + ".json"
    print "writing to ", fname
    json.dump(compositionList, open(fname, "wb"))




if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "midiTojson.py <filename>"
        exit()
    main(sys.argv[1])
