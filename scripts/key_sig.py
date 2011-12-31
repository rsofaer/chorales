from json import load, dump

#Global key_signatures with distributions
key_signatures = load(open('../dataset/key_distributions.json', 'r'))

#Unused
'''
def add_notes(sig):
    n = sig["base_pitch_n"]

    sig["notes"] = set([60+(((n-60))%16), 60+(((n-60)+2)%16),
                    60+(((n-60)+4)%16), 60+(((n-60)+5)%16),
                    60+(((n-60)+7)%16), 60+(((n-60)+9)%16),
                    60+(((n-60)+11)%16), 60+(((n-60)+12)%16)])
    sig["rank"] = 0
'''

#return best keysig given a distribution
def determine_key(l):
    #initializing
    best_score = 100
    best_ans = key_signatures[unicode(0)]

    for key, value in key_signatures.iteritems():
        #epically scoring the thing in one line
        s = sum([abs(a-b) for a,b in zip(l,value['distro'])])
        #print value['base_name'],':',s
        if s < best_score:
            best_score = s
            best_ans = value

    return best_ans

#Determine distribution of notes given melody
#returns the closest key signature
#The parameter voices is [[melody][A][T][B]], but only melody is used
def get_keysig(voices):
    l = [0.0]*20

    #only using melody to create distribution
    for note in voices[0]:
        l[note[u'pitch']-60] += 1.0

    #normalizing
    s = sum(l)
    for i in range(len(l)):
        l[i] = l[i]/s

    #return the keysig with the closest distribution
    return determine_key(l)

#Main function creates distribution JSON for keysigs, then tests
if __name__ == '__main__':

    f = open('../dataset/chorales.json', 'r')
    d = load(f)

    print key_signatures

    #make it like new format
    for key, value in d.iteritems():
        d[key] = [value,[],[],[]]

    #initialize (or empty) distro
    for key, value in key_signatures.iteritems():
        value['distro'] = []


    #calculate distros, add to keysig
    for key, value in d.iteritems():
        l = [0.0]*20
        for note in value[0]:
            #print note
            l[note[u'pitch']-60] += 1.0

        s = sum(l)
        for i in range(len(l)):
            l[i] = l[i]/s

        #print value[0][0][u'keysig']
        key_signatures[unicode(value[0][0][u'keysig'])]['distro'].append(l)

    #combine all distros and normalize
    #what if we didn't average them out?
    #just keep them as is and do a closest-comparison for testing..?-AF
    for key, value in key_signatures.iteritems():
        new_l = [0.0]*20
        for distro in value['distro']:
            for i in range(len(distro)):
                new_l[i] += distro[i]
        #print len(value['distro'])
        for i in range(len(new_l)):
            new_l[i] = new_l[i]/len(value['distro'])

        value['distro'] = new_l
        #print value

    f = open('../dataset/key_distributions.json','w')
    dump(key_signatures, f)

    #test on chorales
    count = 0.0
    tot = 0.0
    for key, value in d.iteritems():
        count += 1.0
        if key_signatures[unicode(value[0][0][u'keysig'])] is get_keysig(value):
            #print True
            tot += 1.0
        '''
        else:
            print key_signatures[unicode(value[0][0][u'keysig'])]
            print get_keysig(value)
        '''
    print str(tot/count * 100.0)+'% Success'
