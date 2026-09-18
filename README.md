# Paper2Agent RF / AWN Demo

A reproducible RF-engineering demonstration of the **Paper2Agent** concept using the Adaptive Wavelet Network (AWN) research paper and its public source code.

This repository is intentionally small. It shows what we built, how the paper-derived capability works, how to interact with it through an agent host such as Codex, how the source workflow was validated, and how to reproduce the experiment without redistributing restricted research assets.

## What we tested

Research paper:

**Jiawei Zhang, Tiantian Wang, Zhixi Feng, Shuyuan Yang (2023)**  
_Toward the Automatic Modulation Classification With Adaptive Wavelet Network_  
DOI: `10.1109/TCCN.2023.3252580`

Source implementation:

- AWN: https://github.com/zjwfufu/AWN
- Pinned commit: `0b3d2b2d3d5d4761e73eb91e223844b4b8585b53`

Conversion framework:

- Paper2Agent: https://github.com/jmiao24/Paper2Agent
- Pinned commit: `8c2d059165ef8cdcb70dbea76655b9c2b55b38e6`

## What was built

The experiment produced a **combined paper-derived research capability** with two parts:

1. **Paper2Skill** — a reviewed agent-readable representation of the full AWN paper for source-grounded reasoning about the method, assumptions, results, figures, and limitations.
2. **Paper2MCP** — a tested MCP server exposing a source-bound executable operation, `awn_evaluate_dataset`, tied to the original AWN implementation.

The MCP capability accepts a supported RadioML dataset and matching pretrained AWN checkpoint, executes the paper-linked evaluation workflow, and returns source-logged metrics, scientific figures, logs, runtime information, and provenance.

## Reference result

Using RML2016.10a and the source-supported pretrained checkpoint:

| Metric | Direct source reference |
|---|---:|
| Accuracy | 62.2023% |
| Macro F1 | 0.641397 |
| Cohen's kappa | 0.584225 |
| Runtime | 24.11 s |

The generated Paper2Agent capability reproduced the direct scientific metrics and scientific output artifacts during independent verification.

## What did we learn?

**Technical feasibility: yes.** A suitable RF-engineering paper with code, data, and a model can be converted into a validated executable research capability.

**Efficiency advantage in this narrow test: not demonstrated.** A prepared direct workflow completed the reuse walkthrough in 111.71 s; the Paper2Agent path took 159.20 s and required one caller-side serialization repair. Scientific quality matched.

That negative result is deliberately preserved. It does not establish that Paper2Agent is generally slower or less useful. It only says that packaging this single AWN benchmark workflow did not reduce effort in this one bounded comparison.

## How do you interact with it?

Paper2Agent does not require a dedicated standalone UI. The interaction layer is normally the **agent host**.

For example, with Codex:

> Use the AWN paper-derived capability to evaluate my supported RadioML2016.10a dataset with this pretrained checkpoint. Report the metrics, show performance by SNR, and explain what the paper says I should and should not infer from the result.

The host can consult the paper skill for research context and invoke the MCP tool for execution.

See [docs/HOW_TO_INTERACT.md](docs/HOW_TO_INTERACT.md), the [recommended first interactive prompt](prompts/EXAMPLE_USE.md), and the [first successful interactive run](examples/FIRST_INTERACTIVE_RUN.md).

## What is not included here

This repository does **not** redistribute:

- the IEEE paper PDF;
- extracted paper text or images;
- RadioML data files;
- AWN pretrained checkpoints;
- generated Python environments;
- the complete combined agent ZIP built from the authorized paper copy.

Those assets retain their original access and licensing terms.

## Reproduce it

Start with [docs/REPRODUCE.md](docs/REPRODUCE.md).

The repository includes:

- exact upstream pins;
- the verified RadioML serialization compatibility script;
- the AWN CPU checkpoint-loading patch used in the experiment;
- the generated MCP wrapper/server source snapshot;
- exact validation results;
- prompts used to rebuild the combined Paper2Agent capability from an authorized local paper copy.

## Scope

This is an offline research reproducibility demonstration using public/synthetic data. It is **not** an operational EW system and does not establish performance on collected operational RF data.

## License

Original code and documentation in this repository are MIT licensed unless otherwise noted. Third-party papers, datasets, source repositories, pretrained models, and other research assets retain their original licenses and terms.
