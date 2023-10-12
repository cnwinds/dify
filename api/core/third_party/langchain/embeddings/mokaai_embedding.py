"""Wrapper around ZhipuAI embedding models."""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator

from langchain.embeddings.base import Embeddings
from langchain.utils import get_from_dict_or_env

from sentence_transformers import SentenceTransformer

class MokaAIEmbeddings(BaseModel, Embeddings):

    client: Any
    model: str
    
    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        print(values)
        if values["client"] is None:
            m = values["model"]
            values["client"] = SentenceTransformer('moka-ai/'+m)
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.client.encode(texts)

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]
