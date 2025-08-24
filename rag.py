from langchain.vectorstores import FAISS
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

def query_rag(querry):
    # Step 1: Load TinyLLaMA model locally
    model_path = "/content/tinyllama"  # Path where you downloaded the model
    tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=True)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    model.eval()

    # Step 2: Load FAISS vector store
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = FAISS.load_local(
        "raj_vector_store",
        embedding_model,
        allow_dangerous_deserialization=True
    )

    # Step 3: Retrieve top 3 relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    docs = retriever.get_relevant_documents(querry)
    context = "\n\n".join([doc.page_content for doc in docs])

    # Step 4: Build prompt
    prompt = f"""You are a helpful assistant trained to answer questions strictly based on the provided Rajkumar's Profile.

    Context:
    {context}

    Question:
    {querry}

    Instructions:
    - If the answer is clearly found in the context, respond accurately and concisely.
    - If the question is unrelated to the context or the answer is not present, respond with:
    "I'm sorry, but this question is outside the scope of the provided Raj's Profile information."

    Answer:"""


    # Tokenize prompt
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    prompt_length = inputs["input_ids"].shape[1]

    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=300,
            do_sample=True,
            top_p=0.95,
            temperature=0.7
        )

    # Decode only the generated part
    generated_ids = outputs[0][prompt_length:]
    generated_text = tokenizer.decode(generated_ids, skip_special_tokens=True)

    print("🧠 Generated Answer:\n")
    print(generated_text)