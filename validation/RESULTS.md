# Validation Results

## Source pins

AWN:

`0b3d2b2d3d5d4761e73eb91e223844b4b8585b53`

Paper2Agent:

`8c2d059165ef8cdcb70dbea76655b9c2b55b38e6`

## Direct source reference

RML2016.10a reference:

| Metric | Result |
|---|---:|
| Accuracy | 0.6220227272727272 |
| Macro F1 | 0.6413968223627294 |
| Cohen's kappa | 0.584225 |
| Runtime | 24.1065 s |

## Compatibility repairs

Two compatibility issues were recorded separately.

### RadioML pickle serialization

The validated reserialized RadioML pickle used Python 3 `str` modulation keys. The pinned AWN loader expected ASCII `bytes` keys.

The compatibility script converted only the key representation and verified:

- 220 modulation/SNR groups;
- all array shapes unchanged;
- all dtypes unchanged;
- `np.array_equal` for every group;
- raw array bytes unchanged;
- semantic dataset hash unchanged.

### CPU checkpoint loading

The source checkpoint load failed on CPU because `torch.load()` attempted CUDA restoration.

A one-line compatibility overlay added:

`map_location=cfg.device`

No model architecture, preprocessing, split logic, metric logic, or scientific parameter was changed.

## Paper2Agent technical result

The combined package passed:

- reviewed Paper2Skill verification;
- source execution comparison;
- independent tool verification;
- changed-input verification;
- failure-case verification;
- MCP integration;
- fresh runtime validation;
- fresh ZIP extraction and delivery validation.

The generated MCP reproduced the direct source metrics and scientific artifacts.

## Narrow reuse comparison

| Measure | Direct workflow | Paper2Agent |
|---|---:|---:|
| Walkthrough wall interval | 111.71 s | 159.20 s |
| Requested successful cases | seed 2022, seed 2024 | same |
| Scientific metrics | matched | matched |
| Scientific SVGs | 44 | same 44 |
| Unsupported scientific claims detected | 0 | 0 |
| New caller repairs | 0 | 1 |

Paper2Agent was 47.48 seconds slower in this one walkthrough.

## Interpretation

The bounded experiment demonstrated **technical feasibility and fidelity**, not an efficiency advantage.

It did not test:

- arbitrary new RF inference;
- multiple paper-derived methods;
- parent-agent method selection;
- cross-paper orchestration;
- analyst-facing EW domain interpretation;
- operational RF data.

Do not generalize this single reuse comparison to other papers or workflows.
