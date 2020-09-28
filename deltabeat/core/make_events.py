from typing import List, Tuple
from .event import Event


def make_atomic_events(positions: List[float]):
    return [Event(pos) for pos in positions]


def make_volume_events(pos_vol_pairs: List[Tuple[float, float]]):
    return [Event(pair[0], volume=pair[1]) for pair in pos_vol_pairs]
