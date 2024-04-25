import logging
import os
from abc import ABC
from typing import Any
from sentence_transformers import SentenceTransformer
import boto3

from fastapi_service.settings.settings import settings, Settings

# LOCAL_MODELS_PATH = os.path.dirname(settings.project.base_dir) + settings.project.model_path
#
logger = logging.getLogger(__name__)


#
# ENDPOINT = "https://console.yandex.cloud/folders/b1gmn7vs5ofi357879d6/storage/buckets/hhbucket"
#
# session = boto3.Session(
#     aws_access_key_id='YCAJEny98L85zWBbOJtoXxhar',
#     aws_secret_access_key='YCPd2nVAFJU7rs1kVESxzzvwmPGt5fk8xtes4li6',
#     region_name="ru-central1",
# )
#
#
# s3 = session.client(
#     "s3", endpoint_url=ENDPOINT)
# s3 = boto3.client('s3',
#
#                   aws_access_key_id="YCAJEny98L85zWBbOJtoXxhar",
#                   aws_secret_access_key="YCPd2nVAFJU7rs1kVESxzzvwmPGt5fk8xtes4li6",)


class AbstractModelGetter(ABC):

    def get_model(self, conf: Settings) -> Any:
        """Get model from S3 if possible
        """

        raise NotImplemented


class ModelLoader(AbstractModelGetter):
    def get_model(self, conf: Settings) -> SentenceTransformer:
        return SentenceTransformer(r'static/model_weights')


def get_transformer() -> SentenceTransformer:
    return ModelLoader().get_model(settings)
