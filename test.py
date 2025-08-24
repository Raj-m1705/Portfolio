from sentence_transformers import SentenceTransformer

# Download and save the model locally
model_name = "sentence-transformers/all-MiniLM-L6-v2"
local_path = "local_embeddings"
model = SentenceTransformer(model_name)
model.save(local_path)
