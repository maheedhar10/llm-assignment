"""
Task 3 - Run one small model locally with Ollama at two quantisation levels and compare
speed (tokens/sec), memory, and output quality on the same 10 prompts.

Usage:
    python task3_benchmark.py                                   # default: Qwen2.5-1.5B fp16 vs q4_K_M
    python task3_benchmark.py qwen2.5:0.5b-instruct-fp16 qwen2.5:0.5b-instruct-q4_K_M   # smaller/faster

Needs: Ollama installed and running (https://ollama.com). Standard library only - no pip installs.
Outputs: results/task3_runs.csv, results/task3_summary.csv, results/task3_outputs.md
"""
import csv
import json
import os
import platform
import subprocess
import sys
import time
import urllib.request

HOST = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODELS = sys.argv[1:] or ["qwen2.5:1.5b-instruct-fp16", "qwen2.5:1.5b-instruct-q4_K_M"]
# temperature 0 + fixed seed => (near) deterministic outputs, so differences come from quantisation, not sampling
OPTIONS = {"temperature": 0, "seed": 42, "num_predict": 256, "num_ctx": 2048}

PROMPTS = [
    {"id": 1, "type": "fact", "prompt": "What is the capital of Australia? Answer in one word.", "expected": "Canberra"},
    {"id": 2, "type": "math word problem", "prompt": "A shop sells pens at 3 for 45 rupees. How much do 7 pens cost? Show your working briefly.", "expected": "105 rupees"},
    {"id": 3, "type": "arithmetic", "prompt": "What is 17 multiplied by 24? Give only the number.", "expected": "408"},
    {"id": 4, "type": "code", "prompt": "Write a Python function is_palindrome(s) that returns True if s is a palindrome, ignoring case and spaces. Code only.", "expected": "correct, runnable function"},
    {"id": 5, "type": "strict JSON", "prompt": "Convert to JSON with keys name, age, city: 'Priya is 28 and lives in Pune.' Output only the JSON.", "expected": '{"name": "Priya", "age": 28, "city": "Pune"}'},
    {"id": 6, "type": "summarisation", "prompt": "Summarise in exactly two sentences: The city council approved a plan to convert three downtown parking lots into public parks. Supporters say the parks will reduce heat and give residents more green space, while some shop owners worry that fewer parking spaces will hurt their business. Construction is expected to begin next spring and finish within eighteen months.", "expected": "2 accurate sentences"},
    {"id": 7, "type": "translation", "prompt": "Translate into French: 'The meeting has been moved to Thursday afternoon.'", "expected": "La réunion a été déplacée à jeudi après-midi."},
    {"id": 8, "type": "format following", "prompt": "List exactly three advantages of solar energy as a numbered list. Nothing else.", "expected": "exactly 3 numbered items"},
    {"id": 9, "type": "logic", "prompt": "If all bloops are razzies and all razzies are lazzies, are all bloops definitely lazzies? Answer yes or no, then explain in one sentence.", "expected": "Yes"},
    {"id": 10, "type": "explanation", "prompt": "Explain what a hash table is to a 10-year-old in under 60 words.", "expected": "simple, correct, < 60 words"},
]


def api(path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(HOST + path, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())


def loaded_model_memory(model):
    """Ollama's own report of memory used by the loaded model (weights + KV cache + buffers)."""
    for m in api("/api/ps").get("models", []):
        if model in (m.get("name"), m.get("model")):
            return m.get("size", 0) / 1e9, m.get("size_vram", 0) / 1e9
    return None, None


def main():
    os.makedirs("results", exist_ok=True)
    print("Machine:", platform.platform(), "|", platform.processor() or platform.machine())
    try:
        api("/api/version")
    except Exception as e:
        sys.exit(f"Ollama is not reachable at {HOST} - start the Ollama app / 'ollama serve' first. ({e})")

    runs, outputs = [], {}
    for model in MODELS:
        print(f"\n=== {model} ===")
        subprocess.run(["ollama", "pull", model], check=True)
        api("/api/generate", {"model": model, "prompt": "Hi", "stream": False,
                              "options": {"num_predict": 4}})          # warm-up: load weights before timing
        outputs[model] = {}
        for p in PROMPTS:
            t0 = time.time()
            r = api("/api/chat", {"model": model, "stream": False, "options": OPTIONS,
                                  "messages": [{"role": "user", "content": p["prompt"]}]})
            wall = time.time() - t0
            gen_tps = r["eval_count"] / (r["eval_duration"] / 1e9)
            prompt_tps = r.get("prompt_eval_count", 0) / max(r.get("prompt_eval_duration", 1) / 1e9, 1e-9)
            mem_total, mem_vram = loaded_model_memory(model)
            text = r["message"]["content"].strip()
            outputs[model][p["id"]] = text
            runs.append({"model": model, "prompt_id": p["id"], "gen_tokens": r["eval_count"],
                         "gen_tok_per_s": round(gen_tps, 2), "prompt_tok_per_s": round(prompt_tps, 2),
                         "wall_s": round(wall, 2), "mem_gb": round(mem_total or 0, 3),
                         "vram_gb": round(mem_vram or 0, 3)})
            print(f"  prompt {p['id']:>2}: {gen_tps:6.1f} tok/s | {r['eval_count']:>3} tokens | mem {mem_total:.2f} GB")
        api("/api/generate", {"model": model, "keep_alive": 0})           # unload so the next model is measured alone
        time.sleep(2)

    with open("results/task3_runs.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(runs[0].keys()))
        w.writeheader()
        w.writerows(runs)

    summary = []
    for model in MODELS:
        rs = [r for r in runs if r["model"] == model]
        tot_tok = sum(r["gen_tokens"] for r in rs)
        summary.append({
            "model": model,
            "mean_gen_tok_per_s": round(sum(r["gen_tok_per_s"] for r in rs) / len(rs), 2),
            "overall_gen_tok_per_s": round(tot_tok / sum(r["gen_tokens"] / r["gen_tok_per_s"] for r in rs), 2),
            "mean_prompt_tok_per_s": round(sum(r["prompt_tok_per_s"] for r in rs) / len(rs), 2),
            "peak_mem_gb": max(r["mem_gb"] for r in rs),
            "peak_vram_gb": max(r["vram_gb"] for r in rs),
            "total_gen_tokens": tot_tok,
        })
    with open("results/task3_summary.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)

    with open("results/task3_outputs.md", "w", encoding="utf-8") as f:
        f.write("# Task 3 - same 10 prompts, two quantisation levels\n\n")
        for p in PROMPTS:
            f.write(f"## Prompt {p['id']} ({p['type']})\n\n**Prompt:** {p['prompt']}\n\n**Expected:** {p['expected']}\n\n")
            for model in MODELS:
                f.write(f"**{model}:**\n\n```\n{outputs[model][p['id']]}\n```\n\n")
            f.write("**My observation:** _write here_\n\n---\n\n")

    print("\nSUMMARY")
    for s in summary:
        print(s)
    print("\nSaved: results/task3_runs.csv, results/task3_summary.csv, results/task3_outputs.md")


if __name__ == "__main__":
    main()
