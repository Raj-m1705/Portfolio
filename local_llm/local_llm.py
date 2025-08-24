import os

# Try to import transformers; if unavailable, provide a deterministic fallback.
try:
    from transformers import pipeline, set_seed
    _has_transformers = True
except Exception:
    _has_transformers = False

_model = os.getenv('LOCAL_LLM_MODEL', 'gpt2')

if _has_transformers:
    try:
        _generator = pipeline('text-generation', model=_model)
    except Exception:
        _generator = None
else:
    _generator = None


def generate_reply(prompt: str, max_length: int = 150) -> str:
    """Generate a reply using local HF pipeline if available, else echo fallback."""
    if _generator:
        try:
            out = _generator(prompt, max_length=max_length, do_sample=True, top_k=50, num_return_sequences=1)
            text = out[0]['generated_text']
            # crude trimming: return the part after the prompt
            if text.startswith(prompt):
                return text[len(prompt):].strip()
            return text.strip()
        except Exception as e:
            return f"[Local generation error: {e}]"

    # Fallback: simple rule-based/echo reply
    if len(prompt) < 40:
        return "Nice! Tell me more — I can also run locally if you install Hugging Face transformers."
    return "I received your message. To enable smarter replies, install `transformers` and set LOCAL_LLM_MODEL in your environment."