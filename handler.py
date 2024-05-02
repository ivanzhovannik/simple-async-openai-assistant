import asyncio
import openai
import time
from abc import ABC, abstractmethod


class BaseOpenAIHandler(ABC):
    @abstractmethod
    def __init__(self, api_key):
        pass


class AsyncOpenAIHandler(BaseOpenAIHandler):
    def __init__(self, api_key):
        self.client = openai.AsyncOpenAI(api_key=api_key)

    async def create_assistant(self, *args, **kwargs):
        return await self.client.beta.assistants.create(*args, **kwargs)

    async def retrieve_assistant(self, assistant_id, *args, **kwargs):
        return await self.client.beta.assistants.retrieve(assistant_id, *args, **kwargs)

    async def list_assistants(self, *args, **kwargs):
        async for assistant in self.client.beta.assistants.list(*args, **kwargs):
            print(assistant.id)

    async def delete_assistant(self, assistant_id, *args, **kwargs):
        return await self.client.beta.assistants.delete(assistant_id, *args, **kwargs)

    async def create_thread(self, *args, **kwargs):
        return await self.client.beta.threads.create(*args, **kwargs)

    async def retrieve_thread(self, thread_id, *args, **kwargs):
        return await self.client.beta.threads.retrieve(thread_id, *args, **kwargs)

    async def list_threads(self, *args, **kwargs):
        async for thread in self.client.beta.threads.list(*args, **kwargs):
            print(thread.id)

    async def delete_thread(self, thread_id, *args, **kwargs):
        return await self.client.beta.threads.delete(thread_id, *args, **kwargs)

    async def create_run(self, thread_id, *args, **kwargs):
        return await self.client.beta.threads.runs.create(thread_id=thread_id, *args, **kwargs)

    async def retrieve_run(self, thread_id, run_id, *args, **kwargs):
        return await self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id, *args, **kwargs)

    async def list_runs(self, *args, **kwargs):
        async for run in self.client.beta.threads.runs.list(*args, **kwargs):
            print(run.id)

    async def delete_run(self, run_id, thread_id, *args, **kwargs):
        return await self.client.beta.threads.runs.delete(run_id, thread_id, *args, **kwargs)
    
    async def list_messages(self, thread_id, *args, **kwargs):
        return await self.client.beta.threads.messages.list(thread_id, *args, **kwargs)

    async def retrieve_run_when_done(self, thread_id, run_id):
        while True:
            run = await self.retrieve_run(thread_id, run_id)
            if run.status in ['completed', 'failed']:
                return run
            await asyncio.sleep(5)


class SyncOpenAIHandler(BaseOpenAIHandler):
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    async def create_assistant(self, *args, **kwargs):
        return self.client.beta.assistants.create(*args, **kwargs)

    async def retrieve_assistant(self, assistant_id, *args, **kwargs):
        return self.client.beta.assistants.retrieve(assistant_id, *args, **kwargs)

    async def list_assistants(self, *args, **kwargs):
        return self.client.beta.assistants.list(*args, **kwargs)

    async def delete_assistant(self, assistant_id, *args, **kwargs):
        return self.client.beta.assistants.delete(assistant_id, *args, **kwargs)

    async def create_thread(self, *args, **kwargs):
        return self.client.beta.threads.create(*args, **kwargs)

    async def retrieve_thread(self, thread_id, *args, **kwargs):
        return self.client.beta.threads.retrieve(thread_id, *args, **kwargs)

    async def list_threads(self, *args, **kwargs):
        return self.client.beta.threads.list(*args, **kwargs)

    async def delete_thread(self, thread_id, *args, **kwargs):
        return self.client.beta.threads.delete(thread_id, *args, **kwargs)

    async def create_run(self, thread_id, *args, **kwargs):
        return self.client.beta.threads.runs.create(thread_id=thread_id, *args, **kwargs)

    async def retrieve_run(self, thread_id, run_id, *args, **kwargs):
        return self.client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id, *args, **kwargs)

    async def list_runs(self, *args, **kwargs):
        return self.client.beta.threads.runs.list(*args, **kwargs)
    
    async def delete_run(self, run_id, thread_id, *args, **kwargs):
        return self.client.beta.threads.runs.delete(run_id, thread_id, *args, **kwargs)

    async def list_messages(self, thread_id, *args, **kwargs):
        return self.client.beta.threads.messages.list(thread_id, *args, **kwargs)
    
    async def retrieve_run_when_done(self, thread_id, run_id):
        while True:
            run = await self.retrieve_run(thread_id, run_id)
            if run.status in ['completed', 'failed']:
                return run
            time.sleep(5)


def define_openai_handler(api_key: str, asynchronous: bool) -> BaseOpenAIHandler:
    if asynchronous:
        return AsyncOpenAIHandler(api_key=api_key)
    else:
        return SyncOpenAIHandler(api_key=api_key)