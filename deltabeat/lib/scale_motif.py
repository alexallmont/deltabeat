from typing import List
import deltabeat as dbt


class ScaleMotif(dbt.Motif):
    """
    Scale an existing motif by a float factor. The resulting motif is scaled
    linearly with the resulting length as original length * factor.
    The naive linear scaling means that the motif's tempo is changed consistently
    throughout, so if a scaled motif is played directly after its original
    source motif, then there will be a noticeable 'jump' in tempo.
    """

    def __init__(self, motif: dbt.Motif, factor: float):
        """
        Create a scaled (time stretched) version of an existing motif.
        :param motif: existing source motif
        :param factor: fractional scaling factor, e.g. 2 gives twice length, half tempo
        """
        if not issubclass(type(motif), dbt.Motif):
            raise dbt.InvalidMotifException(f'Invalid type {type(motif)} for ScaleMotif')

        self.motif = motif
        self.factor = factor

    def length(self) -> float:
        return self.motif.length() * self.factor

    def events(self) -> List[dbt.Event]:
        result = []
        for ev in self.motif.events():
            result.append(ev.clone_at(ev.pos * self.factor))
        return result
