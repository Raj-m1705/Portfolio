from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings  # updated import

# Load extracted text
with open("raj_data.txt", "r", encoding="utf-8") as f:
    policy_text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", " ", ""],
    length_function=len
)

chunks = text_splitter.split_text(policy_text)
print(f"✅ Split into {len(chunks)} chunks.")

# -------------------------------
# Step 3: Create embeddings + FAISS
# -------------------------------
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = FAISS.from_texts(chunks, embedding_model)

# Save FAISS index locally
vector_store.save_local("raj_vector_store")

print("✅ Vector store created and saved locally as 'raj_vector_store'.")