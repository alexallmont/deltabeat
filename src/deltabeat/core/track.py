from .motif import Motif
from .pattern import Pattern


class Track(Pattern):
    """
    A track is a named motif pattern, to which motifs may be dynamically added.
    """

    def __init__(self, name: str):
        """
        Create a new track for dynamically maintaining motifs
        :param name: track name used in multitrack
        """
        super().__init__([])
        self.name = name

    def add_motif(self, motif: Motif):
        self.motifs.append(motif)
