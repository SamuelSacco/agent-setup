# NetworkX — orientation

NetworkX is a Python library for creating, manipulating, and studying
graphs. Package code lives in `networkx/`; import it as
`import networkx as nx`.

## Layout

- `networkx/classes/` — the graph classes (Graph, DiGraph, MultiGraph,
  MultiDiGraph) and their views/filters.
- `networkx/algorithms/` — algorithm subsystems, one package per area
  (centrality, isomorphism, tree, connectivity, ...). Most public
  functions are re-exported through the subsystem `__init__.py` and
  ultimately through `networkx/__init__.py`.
- `networkx/generators/` — graph generators (classic, lattice,
  community, ...).
- `networkx/utils/` — shared machinery: `decorators.py` (argmap,
  not_implemented_for, open_file), `misc.py`, backend dispatch.
- `networkx/readwrite/`, `networkx/drawing/`, `networkx/convert.py` —
  IO, layouts, conversion.
- Tests are colocated: each subsystem has a `tests/` directory next to
  the modules it tests. `networkx/conftest.py` holds shared fixtures.

## Conventions

- Public functions carry numpydoc docstrings, usually with runnable
  examples; keep them accurate when you change behavior.
- User-facing errors use networkx exceptions: `nx.NetworkXError`,
  `nx.NetworkXPointlessConcept`, `nx.NetworkXNoPath`, etc.
- Many public functions are wrapped with decorators from
  `networkx.utils.decorators` (e.g. `@not_implemented_for("directed")`,
  `@nx._dispatchable`). Preserve the wrappers and `__all__` entries.
- Functions that take a `seed` argument use the `np_random` decorator
  pattern; generators return `nx.Graph` objects and honor `seed` for
  reproducibility.
- Match the local style of the file you are editing; the project lints
  with ruff.

## Working

- Run tests targeted, never the whole suite:
  `/home/hatch/workspace/p2/w3/scratch/venv/bin/python -m pytest <path> -q`
  from the repo root. That interpreter has pytest, numpy, and scipy.
- A failing test in the same `tests/` directory as the module you are
  changing is the first thing to explain; a green targeted file is the
  minimum bar before you call a fix done.
- Optional dependencies (pandas, matplotlib, ...) are not installed;
  code paths needing them are skipped in tests and are usually not
  where a core bug lives.
