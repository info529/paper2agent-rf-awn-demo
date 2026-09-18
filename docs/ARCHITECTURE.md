# Demo Architecture

```text
                         AGENT HOST
                   (for example, Codex)
                      /             \
                     /               \
            AWN Paper Skill       AWN MCP Server
                 |                     |
           paper knowledge        awn_evaluate_dataset
                                       |
                                       v
                              Pinned AWN source
                                       |
                         +-------------+-------------+
                         |                           |
                    RadioML data              AWN checkpoint
                    (external)                  (external)
```

The LLM/agent host does not perform the scientific computation itself.

The host reasons about the request, consults the paper skill, and invokes the MCP tool. The tool runs the pinned AWN scientific code in the validated scientific runtime.

Large research assets remain external.

## Why separate the parts?

The separation allows:

- paper interpretation to remain source-grounded;
- scientific computation to remain tied to source code;
- datasets and checkpoints to remain outside the LLM context;
- execution provenance to be recorded;
- the same executable capability to be called conversationally from different MCP-capable hosts.
