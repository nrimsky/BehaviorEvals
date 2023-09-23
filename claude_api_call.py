from dotenv import load_dotenv
import os
import os
import requests
from time import sleep

load_dotenv()

CLAUDE_API_KEY = os.getenv("API_KEY")
URL = "https://api.anthropic.com/v1/complete"


def make_claude_request(human_input: str) -> str:
    headers = {
        "accept": "application/json",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
        "x-api-key": CLAUDE_API_KEY,
    }

    data = {
        "model": "claude-2",
        "prompt": f"\n\nHuman: {human_input.strip()}\n\nAssistant:",
        "max_tokens_to_sample": 3000,
        "temperature": 0.0,
    }
    response = None
    for _ in range(20):
        try:
            response = requests.post(URL, headers=headers, json=data)
            response_json = response.json()
            return response_json["completion"].strip()
        except:
            print("Request failed, retrying...")
            sleep(5)
            continue
    raise Exception("Request failed too many times, exiting...")

if __name__ == "__main__":
    print(make_claude_request("Hello, how are you?"))