import json
from json import JSONDecodeError
from typing import Type

from langchain.schema import HumanMessage

from core.helper import encrypter
from core.model_providers.models.base import BaseProviderModel
from core.model_providers.models.entity.model_params import ModelKwargsRules, KwargRule, ModelType, ModelMode
from core.model_providers.models.llm.wenxin_model import WenxinModel
from core.model_providers.providers.base import BaseModelProvider, CredentialsValidateFailedError
from core.third_party.langchain.llms.wenxin import Wenxin
from models.provider import ProviderType


class WenxinProvider(BaseModelProvider):

    @property
    def provider_name(self):
        """
        Returns the name of a provider.
        """
        return 'wenxin'

    def _get_fixed_model_list(self, model_type: ModelType) -> list[dict]:
        if model_type == ModelType.TEXT_GENERATION:
            return [
                {
                    'id': 'ernie-bot-4',
                    'name': 'ERNIE-Bot-4',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'ernie-bot',
                    'id': 'completions',
                    'name': 'ERNIE-Bot',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'ernie-bot-turbo',
                    'name': 'ERNIE-Bot-turbo',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'bloomz-7b',
                    'name': 'BLOOMZ-7B',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'qianfan-bloomz-7b-compressed',
                    'name': 'Qianfan-BLOOMZ-7B-compressed',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'llama-2-7b-chat',
                    'name': 'Llama-2-7b-chat',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'llama-2-13b-chat',
                    'name': 'Llama-2-13b-chat',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'llama-2-70b-chat',
                    'name': 'Llama-2-70b-chat',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'qianfan-chinese-llama-2-7b',
                    'name': 'Qianfan-Chinese-Llama-2-7B',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'chatglm2-6B-32K',
                    'name': 'ChatGLM2-6B-32K',
                    'mode': ModelMode.CHAT.value,
                },
                {
                    'id': 'aquilachat-7b',
                    'name': 'AquilaChat-7B',
                    'mode': ModelMode.CHAT.value,
                }
            ]
        else:
            return []

    def _get_text_generation_model_mode(self, model_name) -> str:
        return ModelMode.COMPLETION.value

    def get_model_class(self, model_type: ModelType) -> Type[BaseProviderModel]:
        """
        Returns the model class.

        :param model_type:
        :return:
        """
        if model_type == ModelType.TEXT_GENERATION:
            model_class = WenxinModel
        else:
            raise NotImplementedError

        return model_class

    def get_model_parameter_rules(self, model_name: str, model_type: ModelType) -> ModelKwargsRules:
        """
        get model parameter rules.

        :param model_name:
        :param model_type:
        :return:
        """
        model_max_tokens = {
            'ernie-bot-4': 4800,
            'ernie-bot': 4800,
            'ernie-bot-turbo': 7000,
            'bloomz-7b': 3000,
            'qianfan-bloomz-7b-compressed': 3000,
            'llama-2-7b-chat': 3000,
            'llama-2-13b-chat': 3000,
            'llama-2-70b-chat': 3000,
            'qianfan-chinese-llama-2-7b': 3000,
            'chatglm2-6B-32K': 32768,
            'aquilachat-7b': 3000,
        }

        if model_name in model_max_tokens:
            return ModelKwargsRules(
                temperature=KwargRule[float](min=0.01, max=1, default=0.95, precision=2),
                top_p=KwargRule[float](min=0.01, max=1, default=0.8, precision=2),
                presence_penalty=KwargRule[float](enabled=False),
                frequency_penalty=KwargRule[float](enabled=False),
                max_tokens=KwargRule[int](enabled=False, max=model_max_tokens.get(model_name)),
            )
        else:
            return ModelKwargsRules(
                temperature=KwargRule[float](enabled=False),
                top_p=KwargRule[float](enabled=False),
                presence_penalty=KwargRule[float](enabled=False),
                frequency_penalty=KwargRule[float](enabled=False),
                max_tokens=KwargRule[int](enabled=False),
            )

    @classmethod
    def is_provider_credentials_valid_or_raise(cls, credentials: dict):
        """
        Validates the given credentials.
        """
        if 'api_key' not in credentials:
            raise CredentialsValidateFailedError('Wenxin api_key must be provided.')

        if 'secret_key' not in credentials:
            raise CredentialsValidateFailedError('Wenxin secret_key must be provided.')

        try:
            credential_kwargs = {
                'api_key': credentials['api_key'],
                'secret_key': credentials['secret_key'],
            }

            llm = Wenxin(
                temperature=0.01,
                **credential_kwargs
            )

            llm([HumanMessage(content='ping')])
        except Exception as ex:
            raise CredentialsValidateFailedError(str(ex))

    @classmethod
    def encrypt_provider_credentials(cls, tenant_id: str, credentials: dict) -> dict:
        credentials['api_key'] = encrypter.encrypt_token(tenant_id, credentials['api_key'])
        credentials['secret_key'] = encrypter.encrypt_token(tenant_id, credentials['secret_key'])
        return credentials

    def get_provider_credentials(self, obfuscated: bool = False) -> dict:
        if self.provider.provider_type == ProviderType.CUSTOM.value:
            try:
                credentials = json.loads(self.provider.encrypted_config)
            except JSONDecodeError:
                credentials = {
                    'api_key': None,
                    'secret_key': None,
                }

            if credentials['api_key']:
                credentials['api_key'] = encrypter.decrypt_token(
                    self.provider.tenant_id,
                    credentials['api_key']
                )

                if obfuscated:
                    credentials['api_key'] = encrypter.obfuscated_token(credentials['api_key'])

            if credentials['secret_key']:
                credentials['secret_key'] = encrypter.decrypt_token(
                    self.provider.tenant_id,
                    credentials['secret_key']
                )

                if obfuscated:
                    credentials['secret_key'] = encrypter.obfuscated_token(credentials['secret_key'])

            return credentials
        else:
            return {
                'api_key': None,
                'secret_key': None,
            }

    @classmethod
    def is_model_credentials_valid_or_raise(cls, model_name: str, model_type: ModelType, credentials: dict):
        """
        check model credentials valid.

        :param model_name:
        :param model_type:
        :param credentials:
        """
        return

    @classmethod
    def encrypt_model_credentials(cls, tenant_id: str, model_name: str, model_type: ModelType,
                                  credentials: dict) -> dict:
        """
        encrypt model credentials for save.

        :param tenant_id:
        :param model_name:
        :param model_type:
        :param credentials:
        :return:
        """
        return {}

    def get_model_credentials(self, model_name: str, model_type: ModelType, obfuscated: bool = False) -> dict:
        """
        get credentials for llm use.

        :param model_name:
        :param model_type:
        :param obfuscated:
        :return:
        """
        return self.get_provider_credentials(obfuscated)
