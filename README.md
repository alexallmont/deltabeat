# Deltabeat

Compositional tools for time-warped music.

`deltabeat` provides an API for arranging and manipulating musical scores where precise timing is required to match
overlaid rhythms. It provides a way to express motifs as sets of events and programmatically chain them together
to create complex rhythmic structures such as:

- polyrhythms and polymeters
- phased musical scores where two slightly offset phrases need to meet
- tempo shifts between phrases that meet at key musical points
- *tempo rubato* and time slurring with keyframes

The goal of this work is tooling for live performance and practice, built on a core API that provides a graph
structure for scoring and MIDI import and export.
