from functools import lru_cache
from fastapi import Depends
from typing import Annotated

from core.handler import (
    BaseOpenAIHandler,
    AsyncOpenAIHandler,
    SyncOpenAIHandler
)
from config.config import settings


# Define singleton handler to use it as an app dependency
@lru_cache
def get_openai_handler() -> BaseOpenAIHandler:
    api_key = settings.OPENAI_API_KEY
    asynchronous = settings.handler.asynchronous
    if asynchronous:
        return AsyncOpenAIHandler(api_key=api_key)
    else:
        return SyncOpenAIHandler(api_key=api_key)
    

OpenAIHandlerDependency = Annotated[BaseOpenAIHandler, Depends(get_openai_handler)]