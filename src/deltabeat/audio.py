from .motif import MotifType, Source


class AudioSource(Source):
    """
    Audio source data

    Generate audio from imported audio sample data at given sample
    rate. Trim and stretch with standard modifiers.
    """
    def __init__(self, sample_data, sample_rate: int):
        self._sample_rate = sample_rate
        self._sample_data = sample_data
        self._duration = len(self._sample_data) / self._sample_rate

    def type(self) -> MotifType:
        return MotifType.AUDIO

    def count(self) -> int:
        return len(self._sample_data)

    def pos(self, i: int):
        return i / self._sample_rate

    def data(self, i: int):
        return self._sample_data[i]

    def duration(self) -> float:
        return self._duration
