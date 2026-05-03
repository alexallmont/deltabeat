# Deltabeat publish roadmap

This is a resurrection of an old prototype. Before publishing, the goal is to
turn the useful musical idea into a small, clear Python package with a stable
API, modern packaging, good examples, and enough tests to protect the timing
transformations.

Current leaning:

- Use a `src/` layout for package code.
- Collapse the current `core`/`lib` split unless a clearer domain boundary
  emerges; `lib` currently means "concrete motif implementations", which is not
  very helpful to users.
- Keep image rendering available, but consider making Pillow an optional
  dependency if the core package is mainly about event generation.

## Migrate original prototype

- [x] Copy experimental code from local deltabeat-py
- [x] Get examples running (at the moment `PYTHONPATH=src python examples/track_image.py`)

### API and naming

- [x] Adopt motif naming across the API
- [x] Replace `import deltabeat.X` with `import deltabeat as dbt`, i.e. remove `dbc`
- [x] Expose the intended public API from `src/deltabeat/__init__.py`

### Packaging and release

- [x] Move into `src/` structure
- [x] Replace `requirements.txt` with `pyproject.toml`
- [x] Add license
- [x] Add package version and release metadata
- [x] Build wheel and sdist locally
- [x] Check package metadata before upload
- [ ] Publish to PyPI

### Post v0.1 features

- [ ] Introduce pitch/parametric in motif
- [ ] Example complex rhythms and full scores.
- [ ] Import/export midi.
- [ ] Time warp motif.

### Examples and docs

- [ ] Add README quickstart example
- [ ] Add example of pitch change
- [ ] Make image example write an output file instead of only calling `im.show()`
- [ ] Add a short explanation of the core musical model: events, motif length, patterns, tracks, and pitch transforms

### Tests and quality

- [ ] Fix zero-valued event attributes, e.g. `volume=0` and `duration=0`
- [ ] Validate invalid lengths, repeat counts, scale factors, and event positions
- [ ] Add tests for pitch degenerate/error cases
- [ ] Add renderer tests for events without volume
- [ ] Add CI for tests and package build checks
