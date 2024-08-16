from typing import Union
from os import environ
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

API_PREFIX: str = '/api'
ROUTE_PREFIX_V1: str = '/v1'

JWT_TOKEN_PREFIX: str = 'Authorization'

ALLOWED_HOSTS: Union[list[str], None] = environ.get('FASTAPI_ALLOWED_HOSTS', None)
print(ALLOWED_HOSTS)