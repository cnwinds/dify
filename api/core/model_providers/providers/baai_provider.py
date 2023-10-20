from typing import Type

from core.model_providers.models.base import BaseProviderModel
from core.model_providers.models.entity.model_params import ModelKwargsRules, ModelType, ModelMode
from core.model_providers.providers.base import BaseModelProvider

from core.model_providers.models.embedding.baai_embedding import BAAIEmbedding
from core.third_party.langchain.embeddings.baai_embedding import BAAIEmbeddings


class BAAIProvider(BaseModelProvider):

    @property
    def provider_name(self):
        return 'baai'
    
    def _get_text_generation_model_mode(self, model_name) -> str:
        return ModelMode.COMPLETION.value
    
    def _get_fixed_model_list(self, model_type: ModelType) -> list[dict]:
        if model_type == ModelType.EMBEDDINGS:
            return [
                {
                    'id': 'bge-base-zh-v1.5',
                    'name': 'bge-base-zh-v1.5',
                }
            ]
        else:
            return []

    def get_model_class(self, model_type: ModelType) -> Type[BaseProviderModel]:
        if model_type == ModelType.EMBEDDINGS:
            model_class = BAAIEmbedding
        else:
            raise NotImplementedError

        return model_class

    def get_model_parameter_rules(self, model_name: str, model_type: ModelType) -> ModelKwargsRules:
        return ModelKwargsRules()

    @classmethod
    def is_provider_credentials_valid_or_raise(cls, credentials: dict):
        model = BAAIEmbeddings(
            model='bge-base-zh-v1.5',
        )
        model.embed_query("ping")

    @classmethod
    def encrypt_provider_credentials(cls, tenant_id: str, credentials: dict) -> dict:
        return credentials

    def get_provider_credentials(self, obfuscated: bool = False) -> dict:
        return {}

    def should_deduct_quota(self):
        return True

    @classmethod
    def is_model_credentials_valid_or_raise(cls, model_name: str, model_type: ModelType, credentials: dict):
        return

    @classmethod
    def encrypt_model_credentials(cls, tenant_id: str, model_name: str, model_type: ModelType,
                                  credentials: dict) -> dict:
        return {}

    def get_model_credentials(self, model_name: str, model_type: ModelType, obfuscated: bool = False) -> dict:
        return self.get_provider_credentials(obfuscated)
