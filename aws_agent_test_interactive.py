import boto3
import uuid
import sys

# Initialize the runtime client
client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def invoke_my_agent(agent_id, alias_id, session_id):
    print("\n--- Mutual Fund Assistant Active (Type 'exit' to quit) ---")
    
    while True:
        # 1. Ask user for input
        user_input = input("\nYou: ").strip()

        # 2. Check for exit command
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Assistant: Goodbye! Happy investing.")
            break
        
        if not user_input:
            continue

        try:
            # 3. Call Bedrock Agent
            response = client.invoke_agent(
                agentId=agent_id,
                agentAliasId=alias_id,
                sessionId=session_id,
                inputText=user_input
            )

            print("Assistant: ", end="", flush=True)

            # 4. Stream the response chunks
            for event in response.get("completion"):
                if "chunk" in event:
                    chunk_text = event["chunk"]["bytes"].decode("utf-8")
                    print(chunk_text, end="", flush=True)
            print() # New line after response is finished

        except Exception as e:
            print(f"\nError: {str(e)}")

# --- CONFIGURATION ---
# Replace with your actual 10-character Alias ID or 'TSTALIASID'
AGENT_ID = 'TSTALIASID'
ALIAS_ID = 'TSTALIASID'
SESSION_ID = str(uuid.uuid4()) # Keeps track of the conversation context

if __name__ == "__main__":
    invoke_my_agent(AGENT_ID, ALIAS_ID, SESSION_ID)
