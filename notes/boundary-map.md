# Canonical Boundary Map

The AiProjectIntel manifold is only well-defined where boundary conditions are
satisfied. This document is the atlas-level record of every chart boundary:
what keys are required, what models must be accepted, and what hardware the
chart assumes.

---

## Hardware Runtime (measured April 21, 2026)

| Metric | Value |
|--------|-------|
| GPU | NVIDIA GeForce MX550 |
| VRAM | 2.15 GB |
| Driver | 576.83 (CUDA 12.9 max) |
| PyTorch | 2.6.0+cu124 |
| Model | TinyLlama-1.1B-Chat-v1.0 |
| Load time (cold) | 173.4s |
| System RAM (model) | 2.72 GB |
| Throughput | 5.5 tokens/sec (CUDA) |
| Constraint | Models >2GB VRAM must stream or quantize |

---

## Boundary Classes

| Class | Description | Source |
|-------|-------------|--------|
| `API_KEY` | External service credential | Set in `.env` |
| `MODEL_GATE` | HuggingFace gated model license | Accept on hf.co model card |
| `HW_CONSTRAINT` | Hardware requirement | Intel iGPU / NPU / CPU |
| `SVC_RUNTIME` | Local service must be running | e.g. Ollama on :11434 |

---

## Chart Boundary Registry

### AI-Travel-Agent
| Boundary | Class | Status |
|----------|-------|--------|
| `AMADEUS_CLIENT_ID` | API_KEY | ☐ unset |
| `AMADEUS_CLIENT_SECRET` | API_KEY | ☐ unset |
| `SERPAPI_API_KEY` | API_KEY | ☐ unset |
| `SERPER_API_KEY` | API_KEY | ☐ unset |
| Local LLM via llama.cpp SYCL | HW_CONSTRAINT | Intel iGPU required |

### LLM / RAG (open notebooks)
| Boundary | Class | Status |
|----------|-------|--------|
| `HUGGINGFACE_TOKEN` | API_KEY | ✓ live (tjpools) |
| Ollama on localhost:11434 | SVC_RUNTIME | optional (02, 09) |

### LLM / RAG (gated notebooks)
| Boundary | Class | Status |
|----------|-------|--------|
| `HUGGINGFACE_TOKEN` | API_KEY | ✓ live (tjpools) |
| meta-llama/Meta-Llama-3-8B-Instruct | MODEL_GATE | ☐ not accepted |
| meta-llama/Llama-2-7b-chat-hf | MODEL_GATE | ☐ not accepted |
| Intel iGPU (SYCL backend) | HW_CONSTRAINT | 05, 06, 07 |

### Automated-Prompt-Engineering
| Boundary | Class | Status |
|----------|-------|--------|
| `HUGGINGFACE_TOKEN` | API_KEY | ☐ unset |
| Dataset + model download (~GB) | MODEL_GATE | public, no gate |

### Finetune-Image-Captioning
| Boundary | Class | Status |
|----------|-------|--------|
| `HUGGINGFACE_TOKEN` | API_KEY | ☐ unset |
| GPU recommended | HW_CONSTRAINT | Intel iGPU |

### Genre-driven-Storytelling / AI-Web-Language-Tutor
| Boundary | Class | Status |
|----------|-------|--------|
| `HUGGINGFACE_TOKEN` | API_KEY | ☐ unset |

### AI-Upscaling-With-NPU
| Boundary | Class | Status |
|----------|-------|--------|
| Intel NPU driver | HW_CONSTRAINT | NPU required |

### Text-Summarizer-Browser-Plugin
| Boundary | Class | Status |
|----------|-------|--------|
| `HUGGINGFACE_TOKEN` | API_KEY | ☐ unset |
| Browser extension runtime | SVC_RUNTIME | Chrome/Edge |

---

## Activation Order

The manifold becomes progressively defined in this order:

1. `HUGGINGFACE_TOKEN` set → opens all non-gated charts
2. Llama model licenses accepted → opens gated LLM charts
3. Amadeus + SerpAPI keys set → opens AI-Travel-Agent chart
4. Ollama running → opens Ollama-backed charts without HF dependency
5. Intel iGPU drivers installed → opens SYCL/NPU hardware charts

Update Status column (☐ → ✓) as each boundary is made live.
