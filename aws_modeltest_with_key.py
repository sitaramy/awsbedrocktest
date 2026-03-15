import boto3
import os

# 1. Set the specific environment variable Bedrock looks for
# Replace this with your actual ABSK key
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = "LONG_TERM_KEY=="

# 2. Initialize the client WITHOUT passing a token argument
# Boto3 will automatically 'pick up' the key from the environment variable
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# 3. Call the model as usual
try:
    response = client.converse(
        modelId="us.amazon.nova-micro-v1:0",
        messages=[{"role": "user", "content": [{"text": "Hello Nova!"}]}]
    )
    print("Response:", response["output"]["message"]["content"][0]["text"])
except Exception as e:
    print(f"Error: {e}")
