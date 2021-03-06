# This file contains functions to normalize a note in terms of its pitch and time signatures
# Pitch normalization:
# 60 is C4
#
#            8 key signatures
# | N. of sharps | Base Note Name | Base Pitch number
# |  -4          | Ab             | 68
# |  -3          | Eb             | 63
# |  -2          | Bb             | 70
# |  -1          | F              | 65
# |  0           | C              | 60
# |  1           | G              | 67
# |  2           | D              | 62
# |  3           | A              | 69
# |  4           | E              | 64

#
key_signatures = {
    -4: {"base_name": "Ab", "base_pitch_n": 68},
    -3: {"base_name": "Eb", "base_pitch_n": 63},
    -2: {"base_name": "Bb", "base_pitch_n": 70},
    -1: {"base_name": "F",  "base_pitch_n": 65},
     0: {"base_name": "C", "base_pitch_n": 60},
     1: {"base_name": "G", "base_pitch_n": 67},
     2: {"base_name": "D", "base_pitch_n": 62},
     3: {"base_name": "A", "base_pitch_n": 69},
     4: {"base_name": "E", "base_pitch_n": 64},
}

# param note - A note of the form: {"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0},
# return - the new value of note["norm_pitch"], an integer [0..15]
def normalize_pitch(note):
    # Subtract the base pitch of the key signature from the note, then normalize it into the 0-15 range corresponding to 60-75
    norm_pitch = note["pitch"]
    base_pitch = key_signatures[note["keysig"]]["base_pitch_n"]
    while(norm_pitch < base_pitch):
      norm_pitch += 12
    norm_pitch = (norm_pitch - base_pitch)
    note["norm_pitch"] = norm_pitch
    return norm_pitch

# param note - A note of the form: {"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0},
# return - the new value of note["norm_dur"], a number [1/16..1]
def normalize_dur(note):
    note["norm_dur"] = (1.0*note["dur"])/note["timesig"]
    return note["norm_dur"]

# param note - A note of the form: {"st": 8  ,  "pitch": 67,  "dur": 4 ,  "keysig": -1,  "timesig": 12,  "fermata": 0},
# return - the new value of note["pitch"], an integet [60..75]
def denormalize_pitch(note):
    base_pitch = key_signatures[note["keysig"]]["base_pitch_n"]
    note["pitch"] = note["pitch"] + base_pitch
    if(note["pitch"] > 75):
        note["pitch"] -= 12
    return note["pitch"]


# Calls normalize_pitch and normalize_dur
# return - void
def normalize(note):
    normalize_pitch(note)
    #normalize_dur(note)
    return note

def normalize_sequence(sequence):
    return map(normalize, sequence)

# Takes a list of lists of notes and normalizes it.
def normalize_chorale(chorale):
    return map(normalize_sequence, chorale)
