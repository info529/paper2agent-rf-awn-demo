# First Interactive AWN Agent Run

This was the first end-to-end conversational use of the generated AWN paper-derived capability through Codex after the paper skill and MCP server were connected.

## Prompt intent

The host was asked to:

1. explain the AWN paper in plain language for a non-RF specialist;
2. describe what the generated agent can and cannot do;
3. execute the validated `awn_evaluate_dataset` MCP tool;
4. interpret the observed results;
5. distinguish published paper results from the local execution;
6. explain limitations and avoid operational overclaiming.

The full prompt is in [../prompts/EXAMPLE_USE.md](../prompts/EXAMPLE_USE.md).

## Observed execution

The MCP evaluation completed successfully on CPU using:

- dataset: RML2016.10a
- seed: 2022
- pretrained AWN checkpoint
- 44,000 test examples

Observed metrics:

| Metric | Paper result | Interactive execution |
|---|---:|---:|
| Accuracy | 62.44% | 62.20% |
| Macro F1 | 0.6446 | 0.6414 |
| Cohen's kappa | 0.5863 | 0.5842 |

The interactive execution matched the previously validated local reference.

## Plain-language behavior

The host correctly explained that AWN:

- addresses automatic modulation classification;
- operates on short I/Q signal snippets;
- learns signal features using an adaptive wavelet decomposition;
- weights useful features before classification.

It also correctly described the current generated capability boundary:

- paper-grounded explanation: available;
- validated pretrained benchmark evaluation: available;
- training: not exposed;
- arbitrary RF recording classification: not yet exposed;
- individual prediction API: not yet exposed;
- live RF processing: not supported.

## SNR behavior

The run showed the expected pattern that classification performance improves sharply as the signal becomes clearer relative to noise.

Selected observed accuracies:

| SNR | Accuracy |
|---:|---:|
| -20 dB | 9.68% |
| -10 dB | 26.18% |
| -6 dB | 55.00% |
| -2 dB | 81.73% |
| 0 dB | 88.09% |
| 10 dB | 92.23% |
| 16 dB | 92.64% |
| 18 dB | 92.27% |

The host also surfaced class-level differences from the generated scientific artifacts and connected those observations back to the paper's discussion of difficult classes and low-SNR behavior.

## What this demonstrated

This run showed the complete interaction pattern we wanted to test:

```text
paper-derived knowledge
        +
validated executable method
        +
conversational host
        ↓
analyst-facing explanation of an actual scientific run
```

The result is more than paper summarization. The host used the paper skill for explanation, called the generated MCP method, interpreted the resulting scientific artifacts, and kept published results separate from local observations.

## What this did not demonstrate

This run does not establish:

- operational EW performance;
- performance on real intercepted RF;
- generalization to unfamiliar receivers, emitters, or modulation classes;
- transmitter identification or geolocation;
- arbitrary bring-your-own-RF-data inference;
- a time or analyst-effort advantage over direct source use.

Those are separate questions for later experiments.

## Why this matters

The key result of this demo is that a non-specialist can interact with a research-derived RF capability through conversation without manually invoking the underlying Python workflow.

The next meaningful extension is not to repeat the same benchmark. It is to expose and validate source-supported use on new compatible inputs, then add additional paper-derived methods so a parent domain agent can choose among them.
