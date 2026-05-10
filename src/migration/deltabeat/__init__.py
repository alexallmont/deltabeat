from importlib import import_module
from .motif import Motif, MotifType, Source
from .modifier import (
  Modifier,
  Repeat,
  ScalePositions,
  ScaleRate,
  Trim,
  LeftAlign,
  Quantize,
  Swing,
  RateWarp
)
from .midi import (
  MidiSource,
  MidiEdit,
  MidiModifier,
  MidiChannelFilter,
  MidiNoteSubstibute
)


__all__ = [
    "MotifType",
    "Motif",
    "Source",
    "Modifier",
    "Repeat",
    "ScalePositions",
    "ScaleRate",
    "Trim",
    "LeftAlign",
    "Quantize",
    "Swing",
    "RateWarp",
    "MidiSource",
    "MidiEdit",
    "MidiModifier",
    "MidiChannelFilter",
    "MidiNoteSubstibute"
]


def __getattr__(name):
  lazy_exports = {
    "RateWarp": "deltabeat.modifier",
    "load_mid_motif": "deltabeat.midi",
  }

  if name not in lazy_exports:
    raise AttributeError(f"module 'deltabeat' has no attribute {name!r}")

  module_name = lazy_exports[name]
  module = import_module(module_name)
  value = getattr(module, name)
  globals()[name] = value
  return value
