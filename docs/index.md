# AWS Bedrock Testing & Details

Welcome to the technical overview of AWS Bedrock implementation.

## Service Overview
Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, and Meta via a single API.

## Usage & Implementation
To use Bedrock in your application, you can use the Boto3 library in Python.

### Prerequisites
* AWS Account with Bedrock model access enabled.
* IAM permissions for `bedrock:InvokeModel`.

### Sample Code
```python
import boto3

bedrock = boto3.client(service_name='bedrock-runtime')

response = bedrock.invoke_model(
    modelId='anthropic.claude-v2',
    body='{"prompt": "Hello Claude!", "max_tokens_to_sample": 300}'
)