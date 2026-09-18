# How to Interact With the Generated Capability

Paper2Agent does not generate a custom standalone UI for each paper agent.

The usual interaction model is:

```text
You
 |
 v
Agent host (Codex / Claude Code / another MCP-capable host)
 |                      |
 |                      +--> Paper skill
 |                           source-grounded paper knowledge
 |
 +--> MCP server
      executable scientific method
```

The host is the conversational UI.

## Example

After connecting the generated AWN skill and MCP server, an analyst could ask:

> Use the AWN research capability to evaluate my supported RadioML2016.10a dataset with this pretrained checkpoint. Report accuracy, macro F1, Cohen's kappa, and performance by SNR. Then explain what the AWN paper says about the method's assumptions and limitations.

The host can:

1. consult the paper skill;
2. determine whether the executable method applies;
3. invoke `awn_evaluate_dataset`;
4. inspect metrics and artifacts;
5. explain the observed result using the paper context.

## Codex

Paper2Agent's upstream workflow supports Codex as a host.

At a high level:

1. install the generated paper skill under Codex's skill path;
2. install the generated MCP server dependencies;
3. configure Codex to connect to the local STDIO MCP server;
4. start Codex in the analysis workspace;
5. ask normal natural-language questions.

The generated package's `USAGE.md` is the authoritative runtime setup for that exact build.

## Was there a browser UI?

No custom AWN browser application was generated in this experiment.

A future RF/EW domain application could add a UI for:

- dataset selection or upload;
- mission context;
- experiment planning;
- capability selection;
- result visualization;
- provenance;
- chat.

That would be a separate application layer above the paper-derived capabilities.

## Recommended first test

Use the complete walkthrough prompt in [prompts/EXAMPLE_USE.md](../prompts/EXAMPLE_USE.md). It is designed to test the full interaction pattern from plain-language paper explanation through MCP execution and result interpretation.
