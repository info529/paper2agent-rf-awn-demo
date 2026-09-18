# Generated MCP Source Snapshot

This directory contains the small generated MCP layer from the validated experiment.

It does **not** include:

- the AWN source tree;
- RadioML datasets;
- AWN checkpoints;
- the scientific Python environment;
- the paper-derived skill.

To reconstruct the complete validated package, use the reproduction instructions and Paper2Agent with an authorized paper copy.

The MCP wrapper expects the pinned AWN source under its runtime package and requires an explicitly configured Python 3.8 / PyTorch 1.8.1+cpu scientific runtime.

The wrapper deliberately does not:

- train AWN;
- invent an arbitrary RF prediction API;
- normalize datasets silently;
- recompute the scientific metrics independently;
- bundle datasets or checkpoints.
