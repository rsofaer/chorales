import sys, os
import json
import mingus
import mingus.midi.MidiFileIn as mi

'''
File: midiTojson.py
Author: AFlock
Description: turns a midi to a json like we're used to. Requires mingus
'''
def genJson(file):
    try:
        composition = mi.MIDI_to_Composition(file)
    except Exception as e:
        print "Error: ", e


    tempo = composition[1]
    print tempo

    compositionList = []
    for voice in composition[0]:
        if len(voice) is 0:
            continue
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
                noteDict = {"st":st, "pitch" : pitchNum, "dur" : dur, "keysig": None, "timesig" : None, "tempo": tempo, "fermata": 0}
                noteSequence.append(noteDict)
                st += dur

        if len(noteSequence) is not 0:
            compositionList.append(noteSequence)

    return compositionList


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "midiTojson.py <filename> || midiTojson.py 'all' "
        exit()
    if sys.argv[1]:
        if sys.argv[1] is "all":
            datadir = "../dataset/fourPartChorales/"
            filter = "b_.mid"
            allChorales = {}
            for filename in os.listdir(datadir):
                if filter in filename:
                    file = datadir+filename
                    allChorales[filename] = genJson(file)

            fname = "../dataset/fourPartJSON.json"
            print "writing to ", fname
            json.dump(allChorales, open(fname, "wb"))

        else:
            f = sys.argv[1]
            chorale = genJson(f)

            fname = f[:-4] + ".json"

            print "writing to ", fname
            json.dump(chorale, open(fname, "wb"))


