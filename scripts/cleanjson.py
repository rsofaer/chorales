'''
File: cleanjson.py
Author: AFlock
Description: clean up dat json to only what we want
'''

import json

def main():
    """do et"""
    j = json.load(open("../dataset/fourPartJSON.json", "rb"))
    newBoy = {}
    for key, val in j.iteritems():
        #make the magic happen
        tempVoices = []
        for supposedVoice in val:
            if len(supposedVoice)>1:
                #fake voice
                tempVoices.append(supposedVoice)
        if len(tempVoices) is not 4:
            #forget about this shit, it doesn't have 4 voices
            continue
        #otherwise, lets rock
        #the temp voices need to be sorted.

        avgNums = []
        voiceHolder = {}
        #ALott this is what you would put in the function that you sort on VV
        for voice in tempVoices:
            total = 0
            for i, note in enumerate(voice):
                total += note["pitch"]
            avgPitch = float(total)/float(i+1)
            voiceHolder[avgPitch] = voice
            avgNums.append(avgPitch)

        avgNums.sort()
        avgNums.reverse()
        newBoy[key] = []
        for num in avgNums:
            theVoice = voiceHolder[num]
            newBoy[key].append(theVoice)

    #print stats to verify
    print len(newBoy)
    for k, v in newBoy.iteritems():
        print k, "::", len(v)

    json.dump(newBoy, open("../dataset/cleandata.json", "wb"))
    print "success!"

if __name__ == '__main__':
    main()

