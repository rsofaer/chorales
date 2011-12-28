#Import the library
from midiutil.MidiFile import MIDIFile
'''
midify() creates  a midi of the given notes, written to the optional filename
notes is a chorale (a list of dictionaries, with attr. such as u'st', u'pitch',..)
filename is the output name, excluding file extension. it'll be in dataset/midi/
'''
def midify(notes,filename='output'):
    # Create the MIDIFile Object with len(notes) tracks
    MyMIDI = MIDIFile(len(notes))

    for index, note in enumerate(notes):
        
        # Tracks are numbered from zero. Times are measured in beats.
        track = index 
        time = 0
        tempo = 360 #in BPM

        # Add track name and tempo.
        MyMIDI.addTrackName(track,time,"Sample Track "+str(track))
        MyMIDI.addTempo(track,time,tempo)

        #Set fermata duration
        fermata = 2
        
        #Evaluate if fermata is true/false, assign 0 or nonzero value
        fermata = fermata*note[u'fermata']

        # Add a note. addNote expects the following information:
        #track = 0 #set above
        channel = 0
        pitch = note[u'pitch']
        time = note[u'st']
        duration = note[u'dur'] + fermata
        volume = 100

        #not dealt with: timesig, keysig
        
        # Now add the note.
        MyMIDI.addNote(track,channel,pitch,time,duration,volume)
        

    # And write it to disk.
    binfile = open('../dataset/midi/'+filename+".mid", 'wb')
    MyMIDI.writeFile(binfile)
    binfile.close()


if __name__ == '__main__':
    from json import load

    file = open("../dataset/chorales.json")
    data = load(file)
    print 'Total Chorales: ' + str(len(data))
    for key, entry in data.items():
        print 'Generating Chorale ' + key
        midify(entry,'output'+key)
