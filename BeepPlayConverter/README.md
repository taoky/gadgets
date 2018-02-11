This `python` script uses `music21` module to convert music sheets (such as MusicXML, MIDI) to [BeepPlay](https://github.com/iBug/CGadgets/tree/master/BeepPlay)'s format.

(Unstable, and you need to add bpm & offset manually.)

The `samples` directory stores some (almost) successful conversion results. Please note that not all music sheets can convert to listenable Beep songs.

## Limitations:

- Bad support for **chords**.
- Unstable support for **repeats**.
- Only support the first stream.