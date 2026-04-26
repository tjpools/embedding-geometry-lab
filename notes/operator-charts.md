# Operator Charts

Each Intel AI-PC-Samples kit is an operator on the manifold: a map from an
input space to an output space, defined only where its boundary conditions hold.
This document is the atlas of those operators.

---

## Operator: AI-Travel-Agent

```
Domain    → user travel query (natural language)
Range     → structured itinerary (flights, hotels, activities)
Kernel    → LangChain agent + llama.cpp SYCL + tool calls
Tools     → Amadeus (flights/hotels), SerpAPI/Serper (web search), Wikipedia
Entrypoint → AI_Travel_Agent.ipynb  |  AI_Travel_Agent_streamlit.py
Boundaries → AMADEUS_CLIENT_ID, AMADEUS_CLIENT_SECRET,
             SERPAPI_API_KEY or SERPER_API_KEY,
             Intel iGPU (llama.cpp SYCL backend)
```

---

## Operator: LLM-RAG (open)

```
Domain    → document corpus + query
Range     → grounded natural language answer
Kernel    → LangChain RAG chain, vector store, local LLM
Entrypoints → 04_llm-rag.ipynb  |  09_rag_langchain.ipynb
Boundaries → HUGGINGFACE_TOKEN (model download)
             optional: Ollama on localhost:11434
```

---

## Operator: LLM-Inference-SYCL (gated)

```
Domain    → prompt
Range     → generated text
Kernel    → llama.cpp SYCL backend on Intel iGPU
Models    → Meta-Llama-3-8B-Instruct  |  Llama-2-7b-chat-hf
Entrypoints → 05_llm_quantization_sycl.ipynb
              06_llm_sycl_gpu.ipynb
              07_llm_sycl_gpu_python.ipynb
Boundaries → HUGGINGFACE_TOKEN, model license accepted on hf.co,
             Intel iGPU + oneAPI Base Toolkit
```

---

## Operator: Automated-Prompt-Engineering

```
Domain    → task description + candidate prompts
Range     → optimized prompt
Kernel    → iterative LLM evaluation loop
Entrypoint → AutomatedPromptEngineering.ipynb
Boundaries → HUGGINGFACE_TOKEN
             Runtime: pixi (see pixi.toml)
```

---

## Operator: Finetune-Image-Captioning

```
Domain    → image dataset
Range     → fine-tuned vision-language model
Kernel    → HuggingFace Trainer, BLIP/similar architecture
Entrypoint → finetune_image_captioning.ipynb
Boundaries → HUGGINGFACE_TOKEN, Intel iGPU recommended
```

---

## Operator: Genre-driven-Storytelling

```
Domain    → genre tag + seed prompt
Range     → generated narrative
Kernel    → local LLM via llama.cpp or HF pipeline
Entrypoint → Genre-driven-storytelling.ipynb
Boundaries → HUGGINGFACE_TOKEN
```

---

## Operator: AI-Web-Language-Tutor

```
Domain    → user language query
Range     → tutoring response + exercises
Kernel    → LLM + structured prompt scaffolding
Entrypoint → (web app)
Boundaries → HUGGINGFACE_TOKEN
```

---

## Operator: AI-Upscaling-NPU

```
Domain    → low-resolution image
Range     → upscaled image
Kernel    → super-resolution model on Intel NPU
Entrypoint → AI_Upscaling_With_NPU.ipynb
Boundaries → Intel NPU driver (hardware-hard boundary)
```

---

## Operator: Text-Summarizer-Browser-Plugin

```
Domain    → webpage text (browser context)
Range     → summary
Kernel    → local LLM via HF pipeline
Entrypoint → TextSummarizerPlugin.ipynb + browser extension
Boundaries → HUGGINGFACE_TOKEN, Chrome/Edge runtime
```

---

## Composition

Operators can be composed. Natural chains:

- `LLM-RAG → AI-Travel-Agent` — ground the travel agent on a private corpus
- `Automated-Prompt-Engineering → any operator` — optimize prompts before deployment
- `Finetune-Image-Captioning → Genre-driven-Storytelling` — visual narrative pipeline

Composed operators live in `experiments/`.
