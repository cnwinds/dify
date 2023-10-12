from core.third_party.langchain.embeddings.mokaai_embedding import MokaAIEmbeddings

from replicate.exceptions import ModelError, ReplicateError

from core.model_providers.error import LLMBadRequestError
from core.model_providers.providers.base import BaseModelProvider
from core.model_providers.models.embedding.base import BaseEmbedding


class MokaAIEmbedding(BaseEmbedding):
    def __init__(self, model_provider: BaseModelProvider, name: str):
        credentials = model_provider.get_model_credentials(
            model_name=name,
            model_type=""
        )

        client = MokaAIEmbeddings(
            model=name,
        )

        super().__init__(model_provider, client, name)

    def handle_exceptions(self, ex: Exception) -> Exception:
        if isinstance(ex, (ModelError, ReplicateError)):
            return LLMBadRequestError(f"MokaAI embedding: {str(ex)}")
        else:
            return ex
        
    def get_num_tokens(self, text: str) -> int:
        # 使用简单版的计算token方法。
        if len(text) == 0:
            return 0

        return len(text)*2