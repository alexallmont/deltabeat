from importlib import import_module

from .core.event import Event, EventAttributeException
from .core.make_events import make_atomic_events, make_volume_events
from .core.motif import Motif, InvalidMotifException
from .core.multi_track import MultiTrack
from .core.pattern import Pattern
from .core.track import Track
from .lib.custom_motif import CustomMotif
from .lib.pitch_motif import PitchMotif
from .lib.repeat_motif import RepeatMotif
from .lib.scale_motif import ScaleMotif

__all__ = [
    'CustomMotif',
    'Event',
    'EventAttributeException',
    'InvalidMotifException',
    'Motif',
    'MultiTrack',
    'Pattern',
    'PitchMotif',
    'RepeatMotif',
    'ScaleMotif',
    'Track',
    'make_atomic_events',
    'make_volume_events',
    'motif_image',
    'multi_track_image',
]


def __getattr__(name):
    # Lazy load rendering functions to avoid importing Pillow when not needed.
    lazy_exports = {
        'motif_image': ('deltabeat.ui.render', 'motif_image'),
        'multi_track_image': ('deltabeat.ui.render', 'multi_track_image'),
    }

    if name not in lazy_exports:
        raise AttributeError(f"module 'deltabeat' has no attribute {name!r}")

    module_name, attr_name = lazy_exports[name]
    module = import_module(module_name)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value
