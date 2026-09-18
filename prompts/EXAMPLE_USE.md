# Example Interaction

This is the recommended first interactive test after the generated AWN paper skill and MCP server are connected to the host.

The goal is to test the full Paper2Agent interaction pattern:

**paper knowledge → executable method → analyst-facing explanation**

```text
Use the installed AWN paper skill and the connected `awn` MCP server.

Assume I am not an RF engineer.

First, explain in plain English:

1. What problem the AWN paper is trying to solve.
2. What the AWN method actually does.
3. What kind of RF data it works with.
4. What the current AWN paper-derived agent can do.
5. What it cannot do yet.

Then run the validated AWN evaluation using:

Dataset:
/workspaces/research-agent-workbench-ew/upstream/AWN/data/RML2016.10a_dict.pkl

Checkpoint:
/workspaces/research-agent-workbench-ew/upstream/AWN/checkpoint/2016.10a_AWN.pkl

Output directory:
/workspaces/research-agent-workbench-ew/.local-artifacts/interactive-awn/

Use:
- dataset: 2016.10a
- seed: 2022
- device: cpu

After the tool completes, explain the results to me in plain English.

Include:
- accuracy
- macro F1
- Cohen's kappa
- how performance changes with SNR
- where the model appears to perform well or poorly
- what the paper says is important when interpreting those results
- what conclusions I should NOT draw from this benchmark

Clearly distinguish:
- what the paper reports;
- what this execution observed;
- your interpretation.

Do not claim operational RF performance from the RadioML benchmark.
```

## What this prompt tests

A successful interaction should demonstrate that the host can:

1. use the paper skill to explain the research in accessible language;
2. recognize the connected AWN MCP capability;
3. execute the validated scientific method;
4. inspect returned metrics and scientific artifacts;
5. combine source-grounded paper context with observed execution results;
6. preserve the distinction between published results, reproduced results, and model interpretation.

The paths above are specific to the original experiment workspace. Replace them with your own local dataset, checkpoint, and output paths when reproducing the demo.
