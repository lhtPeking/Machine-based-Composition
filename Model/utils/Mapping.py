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
quarter_note_ticks = 240  # 每个八分之一拍的时长

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


# import mido
# from mido import MidiFile, MidiTrack, Message
# import os

# note_map = {
#     "F3": 53, "F#3": 54, "G3": 55, "G#3": 56, "A3": 57, "A#3": 58, "B3": 59,
#     "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66, "G4": 67,
#     "G#4": 68, "A4": 69, "A#4": 70, "B4": 71, "C5": 72, "C#5": 73, "D5": 74, "D#5": 75,
#     "E5": 76, "F5": 77, "F#5": 78, "G5": 79
# }

# # 0为休止符，1-27为音符，28为延音符
# quarter_note_ticks = 240  # 每个八分之一拍的时长

# class Mapping:
#     def __init__(self, sequence, fileName, rank):
#         self.sequence = sequence
#         self.fileName = fileName
#         self.rank = rank

#     def generate(self):
#         midi = MidiFile()
#         track = MidiTrack()
#         midi.tracks.append(track)

#         track.append(mido.MetaMessage('track_name', name='Piano Track'))
#         track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))  # 120BPM

#         time = 0
#         sustain_time = 0

#         for item in self.sequence:
#             if item == 0:  # 休止符
#                 time += quarter_note_ticks
#                 continue
#             elif item == 28:  # 延音符
#                 sustain_time += quarter_note_ticks
#             else:
#                 # 生成和弦
#                 if isinstance(item, str) and item.startswith("C"):  # 如果是和弦标记
#                     chord_type = item[1:]  # 获取和弦类型（如 "M" 表示大三和弦，"m" 表示小三和弦）
#                     root_note = item[0]  # 获取根音
#                     chord_notes = self.generate_chord(root_note, chord_type)
#                     for note in chord_notes:
#                         midi_note = note_map[note]
#                         track.append(Message('note_on', note=midi_note, velocity=64, time=time))
#                         track.append(Message('note_off', note=midi_note, velocity=64, time=quarter_note_ticks + sustain_time))
#                 else:  # 如果是单音符
#                     note_name = list(note_map.keys())[item - 1]
#                     midi_note = note_map[note_name]
#                     track.append(Message('note_on', note=midi_note, velocity=64, time=time))
#                     track.append(Message('note_off', note=midi_note, velocity=64, time=quarter_note_ticks + sustain_time))
#                 time = 0
#                 sustain_time = 0

#         midi.save('../Results/' + self.fileName + '/' + str(self.rank) + '.mid')

#     def generate_chord(self, root_note, chord_type):
#         """
#         根据根音和和弦类型生成和弦音符
#         :param root_note: 根音（如 "C"）
#         :param chord_type: 和弦类型（"M" 表示大三和弦，"m" 表示小三和弦）
#         :return: 和弦音符列表
#         """
#         # 定义音程关系
#         if chord_type == "M":  # 大三和弦
#             intervals = [0, 4, 7]  # 根音、大三度、纯五度
#         elif chord_type == "m":  # 小三和弦
#             intervals = [0, 3, 7]  # 根音、小三度、纯五度
#         else:
#             raise ValueError("不支持的和弦类型")

#         # 获取根音的 MIDI 编号
#         root_midi = note_map[root_note]

#         # 生成和弦音符
#         chord_notes = []
#         for interval in intervals:
#             chord_notes.append(root_midi + interval)

#         # 将 MIDI 编号映射回音符名称
#         chord_note_names = [note for note, midi in note_map.items() if midi in chord_notes]
#         return chord_note_names
