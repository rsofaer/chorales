import sys, os
import json
import mingus
import mingus.midi.MidiFileIn as mi

'''
File: midiTojson.py
Author: AFlock
Description: turns a midi to a json like we're used to. Requires mingus
'''
def main():
    datadir = "../dataset/fourPartChorales/"
    filter = "b_.mid"
    allChorales = {}
    for filename in os.listdir(datadir):
        if filter in filename:
            file = datadir+filename
            try:
                composition = mi.MIDI_to_Composition(file)
            except Error as e:
                print e

            #print composition
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
                compositionList.append(noteSequence)
            allChorales[filename] = compositionList




    fname = "../dataset/fourPartJSON.json"
    print "writing to ", fname
    json.dump(allChorales, open(fname, "wb"))




if __name__ == '__main__':
    main()
