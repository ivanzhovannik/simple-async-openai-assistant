import requests
import argparse
from concurrent.futures import ThreadPoolExecutor

def send_request(n, endpoint):
    messages = [
        {
            "role": "user",
            "content": "You are a math cracker. You reply with numerical value of the problem solution ONLY!"
        },
        {
            "role": "user",
            "content": f"How to solve {n}*sin(x) = cos({n} * x)? "
        }
    ]
    data = {"messages": messages}
    response = requests.post(endpoint, json=data)
    return response.text

def main(n_requests, endpoint):
    with ThreadPoolExecutor(max_workers=n_requests) as executor:
        futures = [executor.submit(send_request, i, endpoint) for i in range(1, n_requests + 1)]
        for future in futures:
            print(future.result())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send multiple concurrent requests to an API.")
    parser.add_argument('n_requests', type=int, help='Number of concurrent requests to send')
    parser.add_argument('endpoint', type=str, help='API endpoint URL')
    args = parser.parse_args()

    main(args.n_requests, args.endpoint)