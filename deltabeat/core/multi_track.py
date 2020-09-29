from .track import Track


class MultiTrack:
    """
    Class for dynamically maintaining a list of tracks
    """

    def __init__(self):
        self.tracks = []

    def add_track(self, name):
        track = Track(name)
        self.tracks.append(track)
        return track

    def num_tracks(self):
        return len(self.tracks)
