import orjson as json
from fastapi import APIRouter, FastAPI, HTTPException
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from app.schema import Query, OutputSchema
from app.dependencies import (
    get_openai_handler,
    OpenAIHandlerDependency
)
from config.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    get_openai_handler()
    try:
        yield
    finally:
        # Clean up resources if necessary
        print("Cleaning up handler")


router = APIRouter(prefix="/api", tags=["assistant"])

@router.post("/query", response_model=OutputSchema)
async def query(query: Query, handler: OpenAIHandlerDependency):
    # Use handler that is injected by Depends
    if not handler:
        raise HTTPException(status_code=503, detail="Server is not ready")

    print(handler)
    try:
        assistant = await handler.create_assistant(
            model=settings.handler.model,
            instructions=settings.handler.system_prompt_template.format(
                output_schema=OutputSchema.schema())
            )
        assistant_id = assistant.id
        print("Assistant ID:", assistant_id)

        thread = await handler.create_thread(messages=query.messages)
        thread_id = thread.id
        print("Thread ID:", thread_id)

        # Create a run and wait for it to complete
        run = await handler.create_run(thread_id=thread_id, assistant_id=assistant_id)
        run_id = run.id
        completed_run = await handler.retrieve_run_when_done(thread_id=thread_id, run_id=run_id)
        print("Run completed:", completed_run)

        # Further processing...
        messages = await handler.list_messages(thread_id)
        response = messages.data[0].content[0].text.value
        
        # Postprocess the string received
        response = json.loads(response.replace("'", '"'))
        return response

    finally:
        if 'assistant_id' in locals():
            await handler.delete_assistant(assistant_id)
        if 'thread_id' in locals():
            await handler.delete_thread(thread_id)