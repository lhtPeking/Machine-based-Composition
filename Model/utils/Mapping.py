import mido
from mido import MidiFile, MidiTrack, Message
import os

note_map = {
    "F3": 53, "F#3": 54, "G3": 55, "G#3": 56, "A3": 57, "A#3": 58, "B3": 59,
    "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66, "G4": 67,
    "G#4": 68, "A4": 69, "A#4": 70, "B4": 71, "C5": 72, "C#5": 73, "D5": 74, "D#5": 75,
    "E5": 76, "F5": 77, "F#5": 78, "G5": 79
}

# 0为休止符，1-27为音符，28为延音符
sequence = [1, 2, 3, 4, 5, 6, 7, 0, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
quarter_note_ticks = 480  # 每个四分之一拍的时长

class Mapping:
    def __init__(self, sequence, fileName, rank):
        self.sequence = sequence
        self.fileName = fileName
        self.rank = rank

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

        midi.save('../Results/' + self.fileName + '/' + str(self.rank) + '.mid')
