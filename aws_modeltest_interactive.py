import boto3
import os
import sys

# 1. Configuration
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = "LONG_TERM_KEY=="
MODEL_ID = "us.amazon.nova-micro-v1:0"

# 2. Initialize Client
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

def start_chat():
    print(f"--- Chatting with {MODEL_ID} (Type 'exit' to stop) ---")
    
    while True:
        # Get input from you
        user_input = input("\nYou: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Prepare message
        messages = [{"role": "user", "content": [{"text": user_input}]}]

        try:
            # 3. Call streaming API
            response = client.converse_stream(
                modelId=MODEL_ID,
                messages=messages,
                inferenceConfig={"maxTokens": 1000, "temperature": 0.7}
            )

            print("Nova: ", end="")
            
            # 4. Handle the stream chunks
            stream = response.get("stream")
            if stream:
                for event in stream:
                    # Look for text deltas in the stream
                    if "contentBlockDelta" in event:
                        text = event["contentBlockDelta"]["delta"]["text"]
                        print(text, end="")
                        sys.stdout.flush() # Force terminal to show text immediately
            print() # New line after response is finished

        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    start_chat()
    
