import math
from PIL import Image, ImageDraw
import typing

from .motif import Motif


line_colours = [(int(255 * i / 7), 127, 255) for i in range(8)]


def motif_image(motif: Motif, scale: int = 100, height: int = 60, col_idx: int = 2):
    width = int(motif.duration() * scale)

    im = Image.new("HSV", (width, height))
    draw = ImageDraw.Draw(im)

    # Draw 'measure' markers to show where pos % 0 == 1
    for d in range(math.ceil(motif.duration())):
        x = float(d * scale)
        draw.line([x, 0, x, height], (0, 0, 40))

    colour = line_colours[col_idx % 8]
    for i in range(motif.count()):
        u = motif.pos(i)
        x = u * scale
        vel = motif.data(i)[2] # FIXME use velocity for debug render
        draw.line([x, height, x, height - height * vel], colour)

    return im.convert("RGB")


# FIXME migrate from old code
@typing.no_type_check
def multi_track_image(multi_track: None, scale: int = 100, track_height: int = 60):
    # Use longest track to determine image width
    max_len = 0
    for track in multi_track.tracks:
        max_len = max(max_len, track.length())
    track_width = max_len * scale

    # Calculate width and height of final image with extra padding
    width = int(track_width + 4)
    height = int((track_height + 2) * multi_track.num_tracks()) + 2

    im = Image.new("RGB", (width, height), (40, 40, 40))
    for i, track in enumerate(multi_track.tracks):
        track_im = motif_image(track, scale, track_height)
        y = i * (track_height + 2) + 2
        im.paste(track_im, (2, y))

    return im
