from typing import List
import deltabeat.core as dbc


class ScaleMotif(dbc.Motif):
    """
    Scale an existing motif by a float factor. The resulting motif is scaled
    linearly with the resulting length as original length * factor.
    The naive linear scaling means that the motif's tempo is changed consistently
    throughout, so if a scaled motif is played directly after its original
    source motif, then there will be a noticeable 'jump' in tempo.
    """

    def __init__(self, motif: dbc.Motif, factor: float):
        """
        Create a scaled (time stretched) version of an existing motif.
        :param motif: existing source motif
        :param factor: fractional scaling factor, e.g. 2 gives twice length, half tempo
        """
        if not issubclass(type(motif), dbc.Motif):
            raise dbc.InvalidMotifException(f'Invalid type {type(motif)} for ScaleMotif')

        self.motif = motif
        self.factor = factor

    def length(self) -> float:
        return self.motif.length() * self.factor

    def events(self) -> List[dbc.Event]:
        result = []
        for ev in self.motif.events():
            result.append(ev.clone_at(ev.pos * self.factor))
        return result
