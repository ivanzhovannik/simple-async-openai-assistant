import argparse
import orjson as json
import requests
from concurrent.futures import ThreadPoolExecutor
from app.schema import OutputSchema


def send_request(n, endpoint):
    schema_example = OutputSchema.schema_json()
    messages = [
        {
            "role": "user",
            "content": "You are a math solver. Please reply using the following JSON format ONLY:\n{schema}".format(schema=schema_example)
        },
        {
            "role": "user",
            "content": "Solve `cos(x) = 1` for x."
        },
        {
            "role": "assistant",
            "content": str(OutputSchema.model_validate({
                "equation": "cos(x) = 1",
                "solution": "2*pi*k, where k is an integer"
            }).json())
        },
        {
            "role": "user",
            "content": "Solve `2 * x = 1` for x."
        },
        {
            "role": "assistant",
            "content": str(OutputSchema.model_validate({
                "equation": "2 * x = 1",
                "solution": 0.5
            }).json())
        },
        {
            "role": "user",
            "content": f"Solve `{n} * sin(x) = 1` for x."
        },
    ]
    data = {"messages": messages}
    response = requests.post(endpoint, json=data)
    return response.text

def main(n_requests, endpoint):
    with ThreadPoolExecutor(max_workers=n_requests) as executor:
        futures = [executor.submit(send_request, i, endpoint) for i in range(1, n_requests + 1)]
        for future in futures:
            print(json.loads(future.result()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send multiple concurrent requests to an API.")
    parser.add_argument('n_requests', type=int, help='Number of concurrent requests to send')
    parser.add_argument('endpoint', type=str, help='API endpoint URL')
    args = parser.parse_args()

    main(args.n_requests, args.endpoint)