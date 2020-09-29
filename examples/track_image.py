from deltabeat.core.make_events import make_volume_events
from deltabeat.core.multi_track import MultiTrack
from deltabeat.lib.custom_beat import CustomBeat
from deltabeat.lib.pitch_beat import PitchBeat
from deltabeat.lib.scale_beat import ScaleBeat
from deltabeat.lib.repeat_beat import RepeatBeat
from deltabeat.ui.render import multi_track_image

motif_2 = CustomBeat(make_volume_events([(i / 16, .7 + i / 100) for i in range(16)]))

mt = MultiTrack()
track_1 = mt.add_track('1')
track_1.add_beat(RepeatBeat(motif_2, 7))

track_2 = mt.add_track('2')
track_2.add_beat(RepeatBeat(motif_2, 2))
track_2.add_beat(PitchBeat(motif_2, 3, 1, 1))
track_2.add_beat(RepeatBeat(motif_2, 2))

track_3 = mt.add_track('3')
track_3.add_beat(RepeatBeat(motif_2, 2))
track_3.add_beat(PitchBeat(motif_2, 3, 1, 2))
track_3.add_beat(ScaleBeat(motif_2, 2))

im = multi_track_image(mt)
im.show()
