import mido
from mido import MidiFile, MidiTrack, Message
import os

note_map = {
    "F3": 173, "F#3": 174, "G3": 175, "G#3": 176, "A3": 177, "A#3": 178, "B3": 179,
    "C4": 180, "C#4": 181, "D4": 182, "D#4": 183, "E4": 184, "F4": 185, "F#4": 186, "G4": 187,
    "G#4": 188, "A4": 189, "A#4": 190, "B4": 191, "C5": 192, "C#5": 193, "D5": 194, "D#5": 195,
    "E5": 196, "F5": 197, "F#5": 198, "G5": 199
}

# 0为休止符，1-27为音符，28为延音符
sequence = [1, 2, 3, 4, 5, 6, 7, 0, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
quarter_note_ticks = 480  # 每个四分之一拍的时长

class Mapping:
    def __init__(self, sequence, fileName):
        self.sequence = sequence
        self.fileName = fileName

    def generate(self):
        midi = MidiFile()
        track = MidiTrack()
        midi.tracks.append(track)

        track.append(mido.MetaMessage('track_name', name='Piano Track'))
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))  # 120BPM

        time = 0
        sustain_time = 0

        for item in self.sequence:
            if item == 0:
                time += quarter_note_ticks
                continue
            elif item == 28:
                sustain_time += quarter_note_ticks
            else:
                note_name = list(note_map.keys())[item - 1]
                midi_note = note_map[note_name]
                track.append(Message('note_on', note=midi_note, velocity=64, time=time))
                track.append(Message('note_off', note=midi_note, velocity=64, time=quarter_note_ticks + sustain_time))  # 结束音符，考虑延音时间
                time = 0
                sustain_time = 0

        midi.save('../../Result/' + self.fileName + '.mid')
