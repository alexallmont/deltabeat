from deltabeat.core.make_events import make_volume_events
from deltabeat.core.multi_track import MultiTrack
from deltabeat.lib.custom_motif import CustomMotif
from deltabeat.lib.pitch_motif import PitchMotif
from deltabeat.lib.scale_motif import ScaleMotif
from deltabeat.lib.repeat_motif import RepeatMotif
from deltabeat.ui.render import multi_track_image

motif_2 = CustomMotif(make_volume_events([(i / 16, .7 + i / 100) for i in range(16)]))

mt = MultiTrack()
track_1 = mt.add_track('1')
track_1.add_motif(RepeatMotif(motif_2, 7))

track_2 = mt.add_track('2')
track_2.add_motif(RepeatMotif(motif_2, 2))
track_2.add_motif(PitchMotif(motif_2, 3, 1, 1))
track_2.add_motif(RepeatMotif(motif_2, 2))

track_3 = mt.add_track('3')
track_3.add_motif(RepeatMotif(motif_2, 2))
track_3.add_motif(PitchMotif(motif_2, 3, 1, 2))
track_3.add_motif(ScaleMotif(motif_2, 2))

im = multi_track_image(mt)
im.show()
