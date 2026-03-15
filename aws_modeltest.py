import boto3
import json
from botocore.exceptions import ClientError

def explore_nova_micro():
    # 1. Initialize the Bedrock Runtime client
    # Nova Micro is available in several regions; us-east-1 is usually a safe bet.
    client = boto3.client("bedrock-runtime", region_name="us-east-1")

    # 2. Define the Model ID
    model_id = "us.amazon.nova-micro-v1:0"

    # 3. Prepare your prompt
    prompt = "Explain why Nova Micro is a great model for developers in 3 short bullet points."

    # 4. Create the message structure for the Converse API
    messages = [
        {
            "role": "user",
            "content": [{"text": prompt}]
        }
    ]

    try:
        # 5. Send the request
        print(f"--- Sending prompt to {model_id} ---")
        response = client.converse(
            modelId=model_id,
            messages=messages,
            inferenceConfig={
                "maxTokens": 500,
                "temperature": 0.7,
                "topP": 0.9
            }
        )

        # 6. Extract and print the response
        output_text = response["output"]["message"]["content"][0]["text"]
        print("\nModel Response:")
        print(output_text)

        # 7. Print token usage (to track your 'exploration' costs)
        usage = response["usage"]
        print(f"\n[Usage Stats]: Input Tokens: {usage['inputTokens']}, Output Tokens: {usage['outputTokens']}")

    except ClientError as e:
        print(f"ERROR: Can't invoke model. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    explore_nova_micro()
