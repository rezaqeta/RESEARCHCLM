
"""
Hash-based Embedding for LlamaIndex
"""

import hashlib
import numpy as np
from llama_index.core.embeddings import BaseEmbedding
from pydantic import Field

class HashEmbedding(BaseEmbedding):
    dim: int = Field(default=384, description="Embedding dimension")
    
    def _get_text_embedding(self, text):
        # Create deterministic embedding using hash
        hash_obj = hashlib.md5(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to numpy array and normalize
        embedding = np.frombuffer(hash_bytes, dtype=np.uint8)
        embedding = np.tile(embedding, (self.dim // len(embedding)) + 1)[:self.dim]
        embedding = embedding.astype(np.float32)
        
        # Normalize
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.tolist()
    
    def _get_text_embeddings(self, texts):
        return [self._get_text_embedding(text) for text in texts]
    
    def _get_query_embedding(self, query):
        return self._get_text_embedding(query)
    
    async def _aget_query_embedding(self, query):
        return self._get_query_embedding(query)
