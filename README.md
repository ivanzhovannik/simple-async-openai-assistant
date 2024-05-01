# simple-async-openai-assistant
Asynchronous FastAPI wrapper for AsyncOpenAI and OpenAI assistantAPI  Resources

## Usage
1. **Add `.secrets.yaml` file to the project root**
```yaml
---
OPENAI_API_KEY: <YOUR_OPENAI_API_KEY>
```

2. **Start the ASGI uvicorn server**:
```python
python app.py
```

3. **Execute <N> api calls concurrently**
```python
python async_query_requests.py <N> http://localhost:8000/api/query
```