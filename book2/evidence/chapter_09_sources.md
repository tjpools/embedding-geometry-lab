# Chapter 9 Source Ledger — Sequence, Memory, and Runtime

**Status:** Source basis established August 14, 2026  
**Scope:** simple recurrent networks, long-range gradient difficulty, LSTM and gated recurrence, and GPU runtime terminology  
**Chapter brief:** [../chapter_briefs/chapter_09.md](../chapter_briefs/chapter_09.md)

## Source Standard

The executable probe is the authority for the chapter's numerical state, sensitivity, and structural-count claims. Historical papers ground lineage and bounded architectural descriptions. Runtime documentation grounds programming-model terms but does not convert the probe into a hardware benchmark.

## Sources

### S1 — Finding Structure in Time

Jeffrey L. Elman, “Finding Structure in Time,” *Cognitive Science* 14, no. 2 (1990): 179–211.

- DOI: https://doi.org/10.1207/s15516709cog1402_1
- Accessed: August 14, 2026
- Authority: primary peer-reviewed recurrent-network paper
- Supports: recurrent processing with internal context over ordered inputs; temporal structure learned through shared network dynamics
- Limitation: The Chapter 9 scalar recurrence is an inspectable teaching model, not a reproduction of Elman's architecture, data, training, or experiments.

### S2 — Learning Long-Term Dependencies Is Difficult

Yoshua Bengio, Patrice Simard, and Paolo Frasconi, “Learning Long-Term Dependencies with Gradient Descent Is Difficult,” *IEEE Transactions on Neural Networks* 5, no. 2 (1994): 157–166.

- DOI: https://doi.org/10.1109/72.279181
- Accessed: August 14, 2026
- Authority: primary peer-reviewed analysis and experiments
- Supports: difficulty of gradient-based learning over long temporal dependencies; repeated propagation can produce decaying influence
- Limitation: The paper's theoretical and empirical scope is broader than the five-step scalar sensitivity product. The probe does not train a network or establish a universal vanishing-gradient result.

### S3 — Long Short-Term Memory

Sepp Hochreiter and Jürgen Schmidhuber, “Long Short-Term Memory,” *Neural Computation* 9, no. 8 (1997): 1735–1780.

- DOI: https://doi.org/10.1162/neco.1997.9.8.1735
- Accessed: August 14, 2026
- Authority: primary peer-reviewed architecture paper
- Supports: LSTM as a gated recurrent architecture designed to address error-flow limitations in recurrent learning
- Limitation: Chapter 9 describes the architectural response historically and does not implement, train, or test an LSTM cell.

### S4 — RNN Encoder-Decoder

Kyunghyun Cho, Bart van Merriënboer, Çaglar Gülçehre, Dzmitry Bahdanau, Fethi Bougares, Holger Schwenk, and Yoshua Bengio, “Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation,” *Proceedings of EMNLP 2014*, 1724–1734.

- URL: https://arxiv.org/abs/1406.1078
- Accessed: August 14, 2026
- Authority: primary peer-reviewed architecture and evaluation paper
- Supports: a gated recurrent encoder-decoder that maps a symbol sequence to a fixed-length vector and decodes another sequence; the historical introduction of the update/reset-gated unit commonly called the GRU
- Limitation: The paper's translation experiment does not establish that every sequence should be compressed into one vector or that the Chapter 9 probe implements its gated unit.

### S5 — CUDA Programming Guide

NVIDIA, “CUDA Programming Guide,” updated May 27, 2026.

- URL: https://docs.nvidia.com/cuda/cuda-programming-guide/
- Accessed: August 14, 2026
- Authority: official programming-model and platform documentation
- Supports: kernels, grids, thread blocks, GPU execution concepts, and the need to distinguish a programming hierarchy from realized performance
- Limitation: The probe launches no CUDA kernel and records no schedule, memory transfer, occupancy, throughput, or timing.

## Claim Matrix

| Claim | Sources | Permitted wording |
|---|---|---|
| Recurrent computation carries step-specific state through an ordered sequence. | S1, probe | In the declared recurrence, each $h_t$ requires $h_{t-1}$ before it can be evaluated. |
| Long paths can make gradient-based learning difficult. | S2, S3 | Products of recurrent derivatives can attenuate or amplify sensitivity; the probe demonstrates one attenuating five-step case only. |
| LSTM and GRU add gates to recurrent computation. | S3, S4 | Gated recurrent architectures were developed to control retention, update, and propagation differently from the simple recurrence. |
| Runtime execution requires mechanisms beyond a mathematical work graph. | S5 | Kernels, scheduling, memory movement, workload, and hardware are required before making a measured performance claim. |

## Prohibited Inferences

The sources and probe do not warrant claims that recurrent state is human memory, every RNN forgets at the same rate, LSTM or GRU eliminates every long-range difficulty, dependency depth equals elapsed time, one recurrent step equals one kernel launch, structural state counts equal measured memory traffic, or attention automatically makes every sequence workload faster.