import json
from json import JSONDecodeError
from typing import Type

from core.model_providers.models.base import BaseProviderModel
from core.model_providers.models.entity.model_params import ModelKwargsRules, ModelType
from core.model_providers.providers.base import BaseModelProvider

from core.model_providers.models.embedding.mokaai_embedding import MokaAIEmbedding
from core.third_party.langchain.embeddings.mokaai_embedding import MokaAIEmbeddings


class MokaAIProvider(BaseModelProvider):

    @property
    def provider_name(self):
        return 'mokaai'

    def _get_fixed_model_list(self, model_type: ModelType) -> list[dict]:
        if model_type == ModelType.EMBEDDINGS:
            return [
                {
                    'id': 'm3e-small',
                    'name': 'm3e-small',
                },
                {
                    'id': 'm3e-base',
                    'name': 'm3e-base',
                },
                {
                    'id': 'm3e-large',
                    'name': 'm3e-large',
                }
            ]
        else:
            return []

    def get_model_class(self, model_type: ModelType) -> Type[BaseProviderModel]:
        if model_type == ModelType.EMBEDDINGS:
            model_class = MokaAIEmbedding
        else:
            raise NotImplementedError

        return model_class

    def get_model_parameter_rules(self, model_name: str, model_type: ModelType) -> ModelKwargsRules:
        return ModelKwargsRules()

    @classmethod
    def is_provider_credentials_valid_or_raise(cls, credentials: dict):
        model = MokaAIEmbeddings(
            model="m3e-base",
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
