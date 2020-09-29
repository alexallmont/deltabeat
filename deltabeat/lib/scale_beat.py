from typing import List
import deltabeat.core as dbc


class ScaleBeat(dbc.Beat):
    """
    Scale an existing beat by a float factor. The resulting beat is scaled
    linearly with the resulting length as original length * factor.
    The naive linear scaling means that the beat's tempo is changed consistently
    throughout, so if a scaled beat is played directly after it's original
    source beat, then there will be a noticeable 'jump' in tempo.
    """

    def __init__(self, beat: dbc.Beat, factor: float):
        """
        Create a scaled (time stretched) version of an existing beat.
        :param beat: existing source beat
        :param factor: fractional scaling factor, e.g. 2 gives twice length, half tempo
        """
        if not issubclass(type(beat), dbc.Beat):
            raise dbc.beat.InvalidBeatException(f'Invalid type {type(beat)} for ScaleBeat')

        self.beat = beat
        self.factor = factor

    def length(self) -> float:
        return self.beat.length() * self.factor

    def events(self) -> List[dbc.Event]:
        result = []
        for ev in self.beat.events():
            result.append(ev.clone_at(ev.pos * self.factor))
        return result
