import deltabeat as dbt

motif_2 = dbt.CustomMotif(dbt.make_volume_events([(i / 16, .7 + i / 100) for i in range(16)]))

mt = dbt.MultiTrack()
track_1 = mt.add_track('1')
track_1.add_motif(dbt.RepeatMotif(motif_2, 7))

track_2 = mt.add_track('2')
track_2.add_motif(dbt.RepeatMotif(motif_2, 2))
track_2.add_motif(dbt.PitchMotif(motif_2, 3, 1, 1))
track_2.add_motif(dbt.RepeatMotif(motif_2, 2))

track_3 = mt.add_track('3')
track_3.add_motif(dbt.RepeatMotif(motif_2, 2))
track_3.add_motif(dbt.PitchMotif(motif_2, 3, 1, 2))
track_3.add_motif(dbt.ScaleMotif(motif_2, 2))

im = dbt.multi_track_image(mt)
im.show()
