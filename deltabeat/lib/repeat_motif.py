from typing import List
import deltabeat.core as dbc


class RepeatMotif(dbc.Motif):
    """
    Repeat an existing motif an integer number of times. The length of the resultant
    motif is the original's length times the number of repeats, i.e. the 'speed' of
    the original motif is maintained.
    """

    def __init__(self, motif: dbc.Motif, repeats: int):
        """
        Create a motif that repeats an existing motif a fixed number of times.
        :param motif: existing source motif
        :param repeats: integral number of repeats
        """
        if not issubclass(type(motif), dbc.Motif):
            raise dbc.InvalidMotifException(f'Invalid type {type(motif)} for RepeatMotif')

        self.motif = motif
        self.repeats = repeats

    def length(self) -> float:
        return self.motif.length() * self.repeats

    def events(self) -> List[dbc.Event]:
        result = []
        for i in range(self.repeats):
            for ev in self.motif.events():
                result.append(ev.clone_at(ev.pos + i * self.motif.length()))
        return result
