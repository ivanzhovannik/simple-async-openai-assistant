# simple-async-openai-assistant
Asynchronous FastAPI wrapper for AsyncOpenAI and OpenAI assistantAPI  Resources

## Usage

### Local

We use [Python3@11](https://www.python.org/downloads/release/python-3110/) for this project. 

1. **Configure your venv and install the requirements**
```shell
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. **Add `.secrets.yaml` file to `config/`**
```yaml
---
OPENAI_API_KEY: <YOUR_OPENAI_API_KEY>
```

3. **Start the ASGI uvicorn server**:
```shell
uvicorn app.main:app --reload --host 0.0.0.0 --port 50050
```

4. **Execute <N> api calls concurrently**
```shell
python async_query_requests.py <N> http://localhost:50050/api/query
```

### Docker

1. **Build the image**:
```shell
docker build -t async-openai-assistant:latest .
```

2. **Run the container**:
```shell
docker run -p 50000:50050 async-openai-assistant:latest
```

3. **Don't forget to set your `config/.secrets.yaml` to enable openai api**
```yaml
docker exec <container_id_or_name> sh -c 'echo "OPENAI_API_KEY: <YOUR_API_KEY_HERE>" > /app/config/.secrets.yaml'
```

4. **Execute <N> api calls concurrently**
```shell
python async_query_requests.py <N> http://<YOUR_HOST>:50000/api/query
```