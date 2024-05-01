from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from contextlib import asynccontextmanager

from config import settings
from handler import AsyncOpenAIHandler

app = FastAPI()

class Query(BaseModel):
    messages: list[dict[str, str]]


@asynccontextmanager
async def get_handler():
    handler = AsyncOpenAIHandler(api_key=settings.OPENAI_API_KEY)
    try:
        yield handler
    finally:
        # Clean up resources if necessary
        print("Cleaning up handler")

# Define a dependency that uses the async context manager
async def dependency():
    async with get_handler() as handler:
        yield handler

@app.post("/api/query")
async def query(query: Query, handler: AsyncOpenAIHandler = Depends(dependency)):
    # Use handler that is injected by Depends
    if not handler:
        raise HTTPException(status_code=503, detail="Server is not ready")

    print(handler)
    try:
        assistant = await handler.create_assistant(model="gpt-4-turbo")
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
        return {'response': response}

    finally:
        if 'assistant_id' in locals():
            await handler.delete_assistant(assistant_id)
        if 'thread_id' in locals():
            await handler.delete_thread(thread_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)