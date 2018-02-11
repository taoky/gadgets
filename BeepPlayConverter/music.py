import music21 as m
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

song = m.converter.parse('music.xml')
# process the ties
song = song.stripTies()

def getMusicProperties(x):
    s = ''
    if (x.isRest):
        s = "0 0 "
    else:
        s = str(x.pitch.pitchClass) + " " + str(x.octave) + " "
    s += str(int(x.duration.quarterLength * 8))
    return s

i = 0
for a in song:
    if a.isStream:
        try:
            e = m.repeat.Expander(a)
            s2 = e.process()
            # timing = s2.secondsMap
            song[i] = s2
        except m.repeat.ExpanderException: # there's no repeat in the stream
            eprint("No repeat in the stream.")
        for b in song[i].recurse().notesAndRests:
            if (b.isNote):
                x = b
                s = getMusicProperties(x)
                print(s)

            if (b.isChord):
                ok = False
                for x in b._notes:
                    if x.pitch == b.root():
                        ok = True
                        s = getMusicProperties(x)
                        print(s)
                        break
                if ok == False:
                    eprint("Warning: Chord")
            if (b.isRest):
                x = b
                s = getMusicProperties(x)
                print(s)
        break
    i += 1
eprint("Finished successfully.")