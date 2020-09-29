from typing import List
import deltabeat.core as dbc


class RepeatBeat(dbc.Beat):
    """
    Repeat an existing beat an integer number of times. The length of the resultant
    beat is the original's length times the number of beats, i.e. the 'speed' of the
    original beat is maintained.
    """

    def __init__(self, beat: dbc.Beat, repeats: int):
        """
        Create a beat that repeats an existing beat a fixed number of times.
        :param beat: existing source beat
        :param repeats: integral number of repeats
        """
        if not issubclass(type(beat), dbc.Beat):
            raise dbc.beat.InvalidBeatException(f'Invalid type {type(beat)} for RepeatBeat')

        self.beat = beat
        self.repeats = repeats

    def length(self) -> float:
        return self.beat.length() * self.repeats

    def events(self) -> List[dbc.Event]:
        result = []
        for i in range(self.repeats):
            for ev in self.beat.events():
                result.append(ev.clone_at(ev.pos + i * self.beat.length()))
        return result
