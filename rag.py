from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# ---- Paths (ensure these exist in ./backend when you deploy) ----
MODEL_PATH = os.getenv("MODEL_PATH", "tinyllama")              # "tinyllama" HF model id or local folder
FAISS_STORE_PATH = os.getenv("FAISS_STORE_PATH", "raj_vector_store")
LOCAL_EMBEDDING_PATH = os.getenv("LOCAL_EMBEDDING_PATH", "local_embeddings")  # local folder or HF id

# ---- Load Model Once ----
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
model.eval()
if torch.cuda.is_available():
    model = model.to("cuda")

# ---- Load Embeddings + Vector Store ----
embedding_model = HuggingFaceEmbeddings(model_name=LOCAL_EMBEDDING_PATH)

# allow_dangerous_deserialization=True is required for FAISS.load_local in many setups
vector_store = FAISS.load_local(
    FAISS_STORE_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

def query_rag(query: str, max_new_tokens: int = 300) -> str:
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # get docs
    docs = retriever.invoke(query)  # new LC pattern
    context = "\n\n".join([doc.page_content for doc in docs]) if docs else ""

    prompt = f"""You are a helpful assistant trained to answer questions strictly based on the provided Rajkumar's Profile.

Context:
{context}

Question:
{query}

Instructions:
- If the answer is clearly found in the context, respond accurately and concisely.
- If the question is unrelated to the context or the answer is not present, respond with:
"I'm sorry, but this question is outside the scope of the provided Raj's Profile information."

Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    prompt_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_p=0.95,
            temperature=0.7
        )

    generated_ids = outputs[0][prompt_length:]
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True).strip()
    return generated_text
