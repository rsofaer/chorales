#Import the library
from midiutil.MidiFile import MIDIFile
import sys
'''
midify() creates  a midi of the given notes, written to the optional filename
notes is a chorale (a list of dictionaries, with attr. such as u'st', u'pitch',..)
filename is the output name, excluding file extension. it'll be in dataset/midi/
'''
def midify(voices,filename='output'):
    # Create the MIDIFile Object with len(notes) tracks
    MyMIDI = MIDIFile(len(voices))

    for jndex, notes in enumerate(voices):
        # Tracks are numbered from zero. Times are measured in beats.
        track = jndex
        time = 0
        tempo = (notes[0][u'tempo'] if u'tempo' in notes[0] else 360) #in BPM

        # Add track name and tempo.
        name = {0:'Soprano',1:'Alto',2:'Tenor',3:'Bass'}[jndex] #:o HAX
        MyMIDI.addTrackName(track,time,name)
        MyMIDI.addTempo(track,time,tempo)

        #Set fermata duration
        fermata = 2

        channel = jndex
        for index, note in enumerate(notes):

            # Add a note. addNote expects the following information:
            #track = 0 #set above

            pitch = note[u'pitch']
            time = note[u'st']
            #fermata is added to duration if it's 1
            duration = note[u'dur'] + (fermata*note[u'fermata'])
            volume = 100

            #not dealt with: timesig, keysig

            # Now add the note.
            MyMIDI.addNote(track,channel,pitch,time,duration,volume)


    # And write it to disk.
    print "Writing MIDI to ../dataset/midi/"+filename+".mid"
    binfile = open('../dataset/midi/'+filename+".mid", 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "midify.py <filename> || midify.py 'all' "
        exit()
    if sys.argv[1]:
        from json import load
        if sys.argv[1] is "all":

            file = open("../dataset/chorales.json")
            data = load(file)
            print 'Total Chorales: ' + str(len(data))
            for key, entry in data.items():
                print 'Generating Chorale ' + key
                midify([entry, [], [], []],'output'+key)

        else:
            fname = sys.argv[1]
            f = open(fname, "rb")

            data = load(f)
            midify(data, 'output'+fname.split('/')[-1].split('.')[0])
