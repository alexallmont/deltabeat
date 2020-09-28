from typing import List
from ..core.beat import Beat
from ..core.event import Event


class RepeatBeat(Beat):
    """
    Repeat an existing beat an integer number of times. The length of the resultant
    beat is the original's length times the number of beats, i.e. the 'speed' of the
    original beat is maintained.
    """

    def __init__(self, beat: Beat, repeats: int = 1):
        self.beat = beat
        self.repeats = repeats

    def length(self) -> float:
        return self.beat.length() * self.repeats

    def events(self) -> List[Event]:
        result = []
        for i in range(self.repeats):
            for ev in self.beat.events():
                result.append(ev.clone_at(ev.pos + i * self.beat.length()))
        return result
