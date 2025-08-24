from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "tinyllama"
FAISS_STORE_PATH = "raj_vector_store"
LOCAL_EMBEDDING_PATH = "local_embeddings"

# Load TinyLLaMA once
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH).eval()
if torch.cuda.is_available():
    model = model.to("cuda")

# Load FAISS with local embeddings
embedding_model = HuggingFaceEmbeddings(model_name=LOCAL_EMBEDDING_PATH)
vector_store = FAISS.load_local(FAISS_STORE_PATH, embedding_model, allow_dangerous_deserialization=True)

def query_rag(query, max_new_tokens=300):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Use invoke() instead of deprecated get_relevant_documents
    docs = retriever.invoke(query)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
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
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    return generated_text
