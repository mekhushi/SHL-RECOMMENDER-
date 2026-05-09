import requests
import json

url = "http://127.0.0.1:8000/chat"

# Simulated conversation based on C1.md
messages = [
    {"role": "user", "content": "We need a solution for senior leadership."}
]

print("--- TURN 1 ---")
resp = requests.post(url, json={"messages": messages})
print(json.dumps(resp.json(), indent=2))

messages.append({"role": "assistant", "content": resp.json().get("reply", "")})
messages.append({"role": "user", "content": "The pool consists of CXOs, director-level postions; people with more than 15 years of experience."})

print("\n--- TURN 2 ---")
resp = requests.post(url, json={"messages": messages})
print(json.dumps(resp.json(), indent=2))

messages.append({"role": "assistant", "content": resp.json().get("reply", "")})
messages.append({"role": "user", "content": "Selection — comparing candidates against a leadership benchmark."})

print("\n--- TURN 3 ---")
resp = requests.post(url, json={"messages": messages})
print(json.dumps(resp.json(), indent=2))
