import boto3
import json

# Initialize the client outside the handler for better performance (warm starts)
client = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name="us-east-1"
)

# Configuration
KNOWLEDGE_BASE_ID = "KB_ID"  # Replace with your actual Knowledge Base ID
MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-lite-v1:0"

def lambda_handler(event, context):
    # 1. Parse details from the Bedrock Agent event
    agent = event['agent']
    action_group = event['actionGroup']
    function = event['function']
    parameters = event.get('parameters', [])
    
    # Extract the query text from the parameters sent by the Agent
    # Assumes your OpenAPI schema defines a parameter named 'query_text'
    query_text = next((p['value'] for p in parameters if p['name'] == 'query_text'), "Summarize documents")

    try:
        # 2. Execute the RAG logic
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
        
        result_text = response['output']['text']
        
    except Exception as e:
        result_text = f"Error querying Knowledge Base: {str(e)}"

    # 3. Format the EXACT response structure Bedrock Agents expect
    response_body = {
        'TEXT': {
            'body': result_text
        }
    }
    
    action_response = {
        'actionGroup': action_group,
        'function': function,
        'functionResponse': {
            'responseBody': response_body
        }
    }
    
    # Return the response to the Agent
    return {
        'response': action_response,
        'messageVersion': '1.0'
    }
