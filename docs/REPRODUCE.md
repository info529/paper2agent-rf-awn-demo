# Reproduce the AWN Paper2Agent Experiment

This guide does not redistribute third-party research assets. Obtain the paper, dataset, and checkpoint under their own terms.

## 1. Use a Linux research environment

The experiment was performed in GitHub Codespaces.

Use a coding-agent host with:

- skills support;
- shell access;
- parallel subagent spawning;
- Python;
- Git.

## 2. Pin Paper2Agent

```bash
git clone https://github.com/jmiao24/Paper2Agent.git
cd Paper2Agent
git checkout 8c2d059165ef8cdcb70dbea76655b9c2b55b38e6
```

For Codex, install the complete Paper2Agent skill:

```bash
mkdir -p "$HOME/.agents/skills/paper2agent"
cp -R skills/paper2agent/. "$HOME/.agents/skills/paper2agent/"
```

Restart the host if necessary.

## 3. Pin AWN

```bash
git clone https://github.com/zjwfufu/AWN.git
cd AWN
git checkout 0b3d2b2d3d5d4761e73eb91e223844b4b8585b53
```

## 4. Obtain the paper

Obtain an authorized local copy of:

_Toward the Automatic Modulation Classification With Adaptive Wavelet Network_  
DOI: `10.1109/TCCN.2023.3252580`

## 5. Obtain RML2016.10a

The experiment used the validated Zenodo distribution:

https://doi.org/10.5281/zenodo.18397070

The optimized pickle uses Python 3 string modulation keys, while the pinned AWN loader expects byte-string keys.

Use:

```bash
python scripts/normalize_rml2016_10a_keys.py \
  --source /path/to/RML2016.10a_dict_optimized.pkl \
  --output /path/to/RML2016.10a_dict.pkl \
  --evidence /path/to/normalization_evidence.json
```

The script verifies that the numeric arrays remain byte-identical after key normalization.

## 6. Obtain the pretrained AWN checkpoint

Use the official pretrained-model source documented by the AWN repository.

The first test used the checkpoint expected as:

`2016.10a_AWN.pkl`

## 7. Apply the CPU compatibility patch if required

The source checkpoint load failed on CPU because `torch.load()` attempted CUDA restoration.

The bounded patch in:

`patches/AWN_CPU_MAP_LOCATION.patch`

adds:

`map_location=cfg.device`

No model architecture or scientific evaluation logic is changed.

## 8. Establish the direct-source reference first

Before agentification, record:

- source commit;
- environment;
- dataset checksum;
- checkpoint checksum;
- command;
- stdout/stderr;
- metrics;
- figures;
- failures and compatibility repairs.

The reference produced in this experiment was:

- Accuracy: `0.6220227272727272`
- Macro F1: `0.6413968223627294`
- Cohen's kappa: `0.584225`

## 9. Run Paper2Agent

See [prompts/BUILD_WITH_PAPER2AGENT.md](../prompts/BUILD_WITH_PAPER2AGENT.md).

The combined route should build:

- a reviewed paper skill;
- a source-bound MCP server;
- independent verification evidence;
- a fresh-runtime/fresh-delivery result.

## 10. Compare reuse

Use the same:

- scientific inputs;
- checkpoint;
- method;
- requested analysis;
- evidence requirements.

Keep one-time construction cost separate from subsequent reuse cost.

See [validation/RESULTS.md](../validation/RESULTS.md).
