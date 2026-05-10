import deltabeat as dbt

midi = dbt.load_mid_motif("simple.mid")
print(midi)
print(midi.duration())
