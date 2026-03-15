import boto3
import os

# 1. Set the Bearer Token for Bedrock Agent Runtime
# Replace with your actual ABSK key
os.environ["AWS_BEARER_TOKEN_BEDROCK"] = "LONG_TERM_KEY=="

# 2. Initialize the Agent Runtime Client
# Note: service_name is 'bedrock-agent-runtime'
client = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name="us-east-1"
)

# 3. Define your Knowledge Base Details
KNOWLEDGE_BASE_ID = "KB_ID"  # Found in Bedrock Console > Knowledge Bases
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0"

def query_knowledge_base(query_text):
    try:
        response = client.retrieve_and_generate(
            input={'text': query_text},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KNOWLEDGE_BASE_ID,
                    'modelArn': MODEL_ARN
                }
            }
        )
        
        # The AI's answer based on your PDFs
        answer = response['output']['text']
        print(f"\nAI Response: {answer}")
        
        # Optional: Print where the info came from (Citations)
        print("\nSources Used:")
        for citation in response.get('citations', []):
            for reference in citation.get('retrievedReferences', []):
                print(f"- {reference['location']['s3Location']['uri']}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    user_query = input("Ask any question about Indian Mutual Funds: ")
    query_knowledge_base(user_query)
