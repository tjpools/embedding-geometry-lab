# AiProjectIntel

## Design Philosophy

This project is built on a discipline borrowed from assembly language programming:
**write to the hardware's designed ability, not against it.**

An assembly programmer's core skill isn't knowing opcodes — it's having an accurate
mental model of the machine. They reason in the hardware's terms: register widths,
cache lines, instruction latency, memory bandwidth. Every decision maps to what the
silicon can actually do.

The same discipline applies here, one level up. The hardware envelope is known and
respected:

| Constraint | Value |
|------------|-------|
| GPU | NVIDIA MX550 |
| VRAM | 2.15 GB |
| Throughput | ~5 tokens/sec |
| Precision | float16 |
| Warm load | ~8.8s |

Models are selected because they **fit the register** — not as toys or demos, but as
properly scaled sections of the same manifold as larger systems. TinyLlama-1.1B runs
the same transformer architecture, the same attention mechanism, the same forward pass
as models 10× or 100× its size. Scaling laws are continuous; this is not a simplified
physics, it is the same physics at a smaller coordinate.

Streaming is enabled because 5 tok/s is a real latency that the UX must respect.
`max_new_tokens` is set because the cost per token on this chip is known. System
prompts are constrained because context window costs VRAM.

**These are not limitations. They are constraint-driven design** — the same conditions
under which the sharpest engineering happens. The abstraction layers above (cloud APIs,
managed endpoints, hosted inference) hide all of this. Here, the full stack is visible
and every number is a real measurement of real hardware.

## Control Hierarchy

A `Ctrl+C` to exit the chat loop is a concrete demonstration of the layered control
stack that governs every inference session:

```
Windows keyboard event
  └─ WSL kernel  →  SIGINT
       └─ Ubuntu process
            └─ zsh terminal session
                 └─ Python process  →  KeyboardInterrupt
                      └─ except block  →  [exit] printed
                           └─ model  (innermost, least privileged)
```

The model generates language about intention and control, but actual control lives in
the layers above it — layers it cannot see and has no representation of. "Exit the
conversation" was never a concept inside the model's context window. It was a meaning
that existed only at the meta-layer: the operating system as controlling overseer.

This is not a flaw in the model. It is the correct architecture. Meaning and control
are properties of the system, not of the innermost component. The assembly programmer
knows this too — the CPU executes instructions but the OS decides when to schedule,
preempt, and terminate the process. The model is the innermost register.

---

A structural atlas for Intel's AI-PC reference kits.

```
pipeline/       tangent bundle   — operators, flows, reference kits (intel/AI-PC-Samples)
environment/    metric tensor    — how the pipeline behaves; venvs, deps, runtimes
experiments/    geodesics        — paths traced through the manifold; your work
notes/          atlas            — coordinate charts, boundary maps, operator specs
.env            chart boundary   — live credentials; gitignored, never committed
.env.example    boundary schema  — the shape of the boundary without values
```

## Activation

```bash
# 1. Set boundary conditions
cp .env.example .env
#    populate .env with real keys

# 2. Enter the metric tensor
source environment/intel-travel/bin/activate

# 3. Navigate
cd pipeline/AI-Travel-Agent
jupyter notebook AI_Travel_Agent.ipynb
```

## Navigation

| Document | Purpose |
|----------|---------|
| [notes/boundary-map.md](notes/boundary-map.md) | Which charts are live, which are degenerate |
| [notes/operator-charts.md](notes/operator-charts.md) | Domain, range, and kernel of each kit |
| [environment/chart-boundaries.env.template](environment/chart-boundaries.env.template) | Full boundary condition reference |

## Status

Manifold is partially defined. HuggingFace boundary → **live (tjpools)**.
Gated model licenses → pending. Travel Agent API keys → pending.
See [notes/boundary-map.md](notes/boundary-map.md) for activation order.
