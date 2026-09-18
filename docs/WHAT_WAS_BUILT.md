# What Was Built

The experiment produced a **combined Paper2Agent capability** for the AWN paper.

## Paper2Skill

The paper component was built from an authorized full-paper copy and independently reviewed.

It preserved source-grounded access to:

- the research problem;
- AWN's contribution;
- adaptive lifting / wavelet decomposition;
- channel attention;
- datasets and assumptions;
- experimental design;
- reported results;
- limitations;
- figures, equations, Algorithm 1, and Table I.

The source PDF and extracted paper assets are not redistributed in this public repository.

## Paper2MCP

The executable component exposed one validated operation:

`awn_evaluate_dataset`

It invokes the original AWN evaluation workflow using supplied native data and a supplied pretrained checkpoint.

Returned outputs include:

- overall accuracy;
- macro F1;
- Cohen's kappa;
- per-SNR confusion matrices;
- accuracy figures;
- source logs;
- stdout/stderr;
- input/config/source hashes;
- runtime and provenance.

## Verification

The generated capability was compared against direct execution of the pinned AWN source.

Verification included:

- direct reference execution;
- changed-seed execution;
- missing-input failure;
- unsupported-dataset failure;
- timeout handling;
- independent implementation verification;
- MCP integration checks;
- fresh-runtime validation;
- fresh ZIP extraction and delivery validation.

The Paper2Agent path reproduced the direct source metrics and scientific artifacts.

## Important boundary

The generated MCP operation was intentionally scoped to **pretrained evaluation**.

It does not currently expose:

- arbitrary RF sample prediction as a separate inference API;
- model training;
- fine-tuning;
- emitter identification;
- threat identification;
- arbitrary operational RF analysis.

The underlying AWN model contains a prediction path, but exposing that for new analyst-supplied IQ samples would require a separate source-backed interface and independent validation.

This repository demonstrates a paper-derived executable research capability, not a complete EW agent.
