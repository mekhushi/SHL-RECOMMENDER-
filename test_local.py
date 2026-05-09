from schemas import ChatRequest, Message
from data_loader import CatalogManager
from agent import SHLAgent
from dotenv import load_dotenv

load_dotenv()

catalog_mgr = CatalogManager("catalog.json")
agent = SHLAgent(catalog_mgr)

print("Testing the agent locally...\n")

# Simulated conversation based on C1.md
messages = [
    Message(role="user", content="We need a solution for senior leadership.")
]

print("--- TURN 1 ---")
resp = agent.process_chat(ChatRequest(messages=messages))
print(f"Reply: {resp.reply}")
print(f"Recommendations: {resp.recommendations}")
print(f"End of conversation: {resp.end_of_conversation}\n")

messages.append(Message(role="assistant", content=resp.reply))
messages.append(Message(role="user", content="The pool consists of CXOs, director-level postions; people with more than 15 years of experience."))

print("--- TURN 2 ---")
resp = agent.process_chat(ChatRequest(messages=messages))
print(f"Reply: {resp.reply}")
print(f"Recommendations: {resp.recommendations}")
print(f"End of conversation: {resp.end_of_conversation}\n")

messages.append(Message(role="assistant", content=resp.reply))
messages.append(Message(role="user", content="Selection — comparing candidates against a leadership benchmark."))

print("--- TURN 3 ---")
resp = agent.process_chat(ChatRequest(messages=messages))
print(f"Reply: {resp.reply}")
print(f"Recommendations: {resp.recommendations}")
print(f"End of conversation: {resp.end_of_conversation}\n")
