import requests
import json
import time

url = "http://127.0.0.1:8000/chat"
messages = []

print("="*60)
print("SHL Assessment Recommender - Interactive Chat")
print("Type 'exit' or 'quit' to stop.")
print("="*60)

while True:
    user_input = input("\n You: ")
    if user_input.lower() in ['exit', 'quit']:
        break
        
    messages.append({"role": "user", "content": user_input})
    
    print(" Agent is thinking...")
    try:
        start_time = time.time()
        resp = requests.post(url, json={"messages": messages})
        data = resp.json()
        end_time = time.time()
        
        reply = data.get("reply", "")
        recommendations = data.get("recommendations", [])
        end_conv = data.get("end_of_conversation", False)
        
        print(f"\n Agent ({round(end_time - start_time, 2)}s): {reply}")
        
        if recommendations:
            print("\n Recommended Assessments:")
            for i, rec in enumerate(recommendations, 1):
                print(f"  {i}. {rec.get('name')} - {rec.get('url')}")
                
        messages.append({"role": "assistant", "content": reply})
        
        if end_conv:
            print("\n  The agent considers this conversation fully complete.")
            
    except Exception as e:
        print(f" Error connecting to server: {e}")
        messages.pop() # Remove the last user message so we can retry

print("\nGoodbye!")
