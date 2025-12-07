import os
import re
import asyncio
import requests
from typing import Optional

# NOTE:
# This version uses the Hugging Face Inference API so you can use free/community-hosted
# models (or HF's free tier). Create a free Hugging Face account and set:
#
#   HF_API_TOKEN (environment variable)
#
# Models used here are examples. You can swap `MODEL_LOGIC`, `MODEL_SAFETY`,
# and `MODEL_HUMANITY` to other models available on https://huggingface.co/models.

# --- 1. CONFIGURE (Hugging Face) MODELS ---
HF_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_TOKEN:
    # We don't raise here to keep UX smooth; requests will fail if token missing.
    print("Warning: HF_API_TOKEN not set. Hugging Face Inference calls will likely fail.")

# Example models (instruction-capable / smaller models suitable for free-tier use)
MODEL_LOGIC = "google/flan-t5-large"        # MELCHIOR - logical / reasoning
MODEL_SAFETY = "bigscience/bloomz-1b1"     # BALTHASAR - pragmatic / safety
MODEL_HUMANITY = "google/flan-t5-small"    # CASPER - humanist / intuitive

HF_API_URL = "https://api-inference.huggingface.co/models"

def _hf_post_sync(model_id: str, prompt: str, max_length: Optional[int] = 256):
    """Synchronous POST to Hugging Face Inference API. Wrapped in asyncio with to_thread."""
    headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": max_length}}
    resp = requests.post(f"{HF_API_URL}/{model_id}", json=payload, headers=headers, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    # Response formats vary by model and HF runtime. Try common possibilities.
    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(f"HF inference error: {data['error']}")
    if isinstance(data, list) and len(data) and isinstance(data[0], dict) and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    # Some endpoints return plain text
    if isinstance(data, str):
        return data
    # Fallback: stringify JSON
    return str(data)

# --- 2. DEFINE THE 3 AI AGENTS (as async functions) ---

async def query_melchior(prompt: str) -> str:
    """The Scientist - uses an instruction-following HF model for logical reasoning.

    Runs the HF call in a thread so it can be awaited concurrently with other agents.
    """
    system_prompt = "You are MELCHIOR, a purely logical analyst. Answer succinctly and conclude with 'DECISION: [YES/NO]'.\n\n" \
                    f"Question: {prompt}\n"
    return await asyncio.to_thread(_hf_post_sync, MODEL_LOGIC, system_prompt)

async def query_balthasar(prompt: str) -> str:
    """The Mother/Pragmatist - pragmatic/safety-focused HF model."""
    system_prompt = "You are BALTHASAR, a protective and pragmatic advisor. Answer with practical concerns and conclude with 'DECISION: [YES/NO]'.\n\n" \
                    f"Question: {prompt}\n"
    return await asyncio.to_thread(_hf_post_sync, MODEL_SAFETY, system_prompt)

async def query_casper(prompt: str) -> str:
    """The Humanist/Intuitive - uses a more conversational HF model."""
    system_prompt = "You are CASPER, an empathetic and intuitive advisor. Speak from the heart and conclude with 'DECISION: [YES/NO]'.\n\n" \
                    f"Question: {prompt}\n"
    return await asyncio.to_thread(_hf_post_sync, MODEL_HUMANITY, system_prompt)

# --- 3. THE ORCHESTRATOR AND VOTING ---

def parse_vote(response_text):
    """Finds the 'DECISION: YES' or 'DECISION: NO' in the text"""
    match = re.search(r"DECISION:\s*(YES|NO)", response_text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "ABSTAIN" # If the AI fails to follow instructions

async def run_magi_system(main_question):
    print(f"--- ❓ MAGI QUERY --- \n{main_question}\n")
    
    # Run all three AI queries in parallel
    tasks = [
        query_melchior(main_question),
        query_balthasar(main_question),
        query_casper(main_question)
    ]
    responses = await asyncio.gather(*tasks)
    
    melchior_response, balthasar_response, casper_response = responses

    # Parse the votes
    votes = {
        "MELCHIOR": parse_vote(melchior_response),
        "BALTHASAR": parse_vote(balthasar_response),
        "CASPER": parse_vote(casper_response)
    }

    print("--- 🗳️ VOTES ---")
    print(f"MELCHIOR (Logic): {votes['MELCHIOR']}")
    print(f"BALTHASAR (Safety): {votes['BALTHASAR']}")
    print(f"CASPER (Humanity): {votes['CASPER']}\n")

    # Tally the votes
    vote_list = list(votes.values())
    yes_votes = vote_list.count("YES")
    no_votes = vote_list.count("NO")

    final_decision = "INCONCLUSIVE"
    if yes_votes >= 2:
        final_decision = "PASSED"
    elif no_votes >= 2:
        final_decision = "REJECTED"

    print(f"--- 🏛️ FINAL DECISION: {final_decision} ---")

    # Optional: Print the full reasoning
    # print("\n--- REASONING ---")
    # print(f"\n[MELCHIOR]:\n{melchior_response}")
    # print(f"\n[BALTHASAR]:\n{balthasar_response}")
    # print(f"\n[CASPER]:\n{casper_response}")

    return final_decision

# --- 4. RUN IT ---
if __name__ == "__main__":
    question = "Should we shut down the server for 15 minutes during peak hours to apply a critical security patch that plugs a 0-day exploit?"
    
    # Use asyncio.run() to execute the main async function
    asyncio.run(run_magi_system(question))