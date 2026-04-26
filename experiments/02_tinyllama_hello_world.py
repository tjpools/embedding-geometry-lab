"""
Experiment 02 — Hello World
============================
Model:   TinyLlama-1.1B-Chat-v1.0 (local cache, no download)

Experiment 01 characterized the hardware envelope:
  GPU:        MX550, 2.15 GB VRAM
  Load time:  ~8.8s (warm cache)
  Throughput: ~5 tokens/sec on CUDA

This experiment is the clean inference path:
  - Streaming output  (tokens print as they arrive — essential at 5 tok/s)
  - System prompt     (gives the model a defined role)
  - Interactive loop  (load once, query many times)

Run:  python experiments/02_tinyllama_hello_world.py
Exit: type 'quit', 'exit', or press Ctrl+C
"""

import os
import torch
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

# ── 1. Boundary: HF token ──────────────────────────────────────────────────────
load_dotenv('/home/tjpools/AiProjectIntel/.env')
token = os.getenv('HUGGINGFACE_TOKEN') or os.getenv('HF_TOKEN')

# ── 2. Load model from warm cache ─────────────────────────────────────────────
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
device   = "cuda" if torch.cuda.is_available() else "cpu"

print(f"[load] {MODEL_ID} — device: {device.upper()}")
print("       loading from cache (~8s)...\n")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, token=token)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    token=token,
    torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    low_cpu_mem_usage=True,
)
model.to(device)
model.eval()

print("[ready] Model loaded. Type a message. ('quit' to exit)\n")
print("─" * 60)

# ── 3. System prompt ──────────────────────────────────────────────────────────
SYSTEM = (
    "You are a concise, helpful assistant running on a local GPU. "
    "Keep responses short and clear."
)

# ── 4. Streamer — prints tokens as they are generated ─────────────────────────
streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)

# ── 5. Interactive chat loop ───────────────────────────────────────────────────
while True:
    try:
        user_input = input("\nYou: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[exit]")
        break

    if not user_input:
        continue
    if user_input.lower() in {"quit", "exit", "q"}:
        print("[exit]")
        break

    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user",   "content": user_input},
    ]
    input_text = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    inputs = tokenizer(input_text, return_tensors="pt").to(device)

    print("\nAssistant: ", end="", flush=True)
    with torch.no_grad():
        model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            streamer=streamer,
            pad_token_id=tokenizer.eos_token_id,
        )
