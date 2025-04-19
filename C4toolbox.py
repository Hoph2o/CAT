# -*- coding: utf-8 -*-
from reaper_python import *

# Map instrument names to REAPER track objects
array_instruments = {}

def startup():
    """
    Populates array_instruments with references to the first 4 tracks:
    Drums, Guitar, Bass, Keys (in that order).
    """
    global array_instruments
    array_instruments = {
        "Drums": RPR_GetTrack(0, 0),
        "Guitar": RPR_GetTrack(0, 1),
        "Bass": RPR_GetTrack(0, 2),
        "Keys": RPR_GetTrack(0, 3)
    }

def add_od(track_name, length_beats, frequency_beats, start_beat=0):
    """
    Inserts overdrive notes into 'PART {track_name}' within the existing MIDI note range.
    """

    target_name = "PART {}".format(track_name.upper())
    track = None

    # Search for target track
    for i in range(RPR_CountTracks(0)):
        t = RPR_GetTrack(0, i)
        name = RPR_GetTrackName(t, "", 512)[2].strip()

        if name.upper() == target_name:
            track = t
            break

    # Get the first MIDI item/take
    take = None
    midi_item = None
    for i in range(RPR_CountTrackMediaItems(track)):
        item = RPR_GetTrackMediaItem(track, i)
        temp_take = RPR_GetMediaItemTake(item, 0)
        if temp_take and RPR_TakeIsMIDI(temp_take):
            take = temp_take
            midi_item = item
            break

    # Get bounds of existing MIDI notes
    note_count = RPR_MIDI_CountEvts(take, 0, 0, 0)[2]

    min_ppq = None
    max_ppq = None

    for i in range(note_count):
        note_info = RPR_MIDI_GetNote(take, i, 0, 0, 0.0, 0.0, 0, 0, 0)
        if note_info[0]:
            startppq = int(note_info[5])
            endppq = int(note_info[6])
            if min_ppq is None or startppq < min_ppq:
                min_ppq = startppq
            if max_ppq is None or endppq > max_ppq:
                max_ppq = endppq

    # Insert new overdrive notes within bounds
    ppq_per_beat = 480
    ppq_len = int(length_beats * ppq_per_beat)
    ppq_step = int(frequency_beats * ppq_per_beat)

    # Start notes after the first note + frequency
    pos = min_ppq + ppq_step
    inserted = 0

    while pos + ppq_len <= max_ppq and inserted < 300:
        RPR_MIDI_InsertNote(take, False, False, pos, pos + ppq_len, 0, 116, 100, False)
        pos += ppq_step
        inserted += 1
