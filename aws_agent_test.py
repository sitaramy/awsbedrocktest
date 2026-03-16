import boto3
import uuid

# Initialize the runtime client
client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

def ask_agent(prompt, agent_id, agent_alias_id, session_id):
    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=agent_alias_id,
        sessionId=session_id, # Use same ID to maintain conversation history
        inputText=prompt
    )

    full_response = ""
    
    # Iterate through the event stream
    for event in response.get("completion"):
        if "chunk" in event:
            chunk = event["chunk"]
            full_response += chunk["bytes"].decode("utf-8")
        elif "trace" in event:
            # Optional: Print reasoning trace if enabled in invoke_agent
            pass

    return full_response

# Usage
my_agent_id = 'TSTALIASID'
my_alias_id = 'TSTALIASID'
session = str(uuid.uuid4()) # Unique ID for this specific chat session

print(ask_agent("Whats the latest NAV of scheme code 119598 ?", my_agent_id, my_alias_id, session))
