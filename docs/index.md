# Mutual Fund Advisory Service | Use Case Details

Build a mutual fund advisory service that will pull basic mutual funds details of all AMCs from the MF fact sheets. For a given MF, it searches for scheme code for a given MF scheme name, searches for its NAV, shows historical NAV and does mutual fund analysis.

## Technical Summary

This technical summary outlines the architecture of a sophisticated AI Investment Assistant built on AWS. The system orchestrates between static document intelligence (RAG) and real-time financial data (Action Groups).

### Technical Architecture Overview: Mutual Fund AI Assistant

The solution utilizes a "ReAct" (Reasoning and Acting) orchestration pattern powered by Amazon Nova Pro, balancing document retrieval with real-time API execution.

#### 1. Knowledge Base (RAG) with S3 Vector Store

- **Data Source:** PDF Factsheets stored in Amazon S3. These documents contain static fund data: investment objectives, category definitions, and risk-o-meters.
- **Vector Storage:** Instead of external clusters, the KB uses Bedrock’s managed vector store backed by S3.

**Ingestion Pipeline:**

- **S3 Sync:** Documents are pulled directly from the source bucket.
- **Embedding Model:** Text chunks are transformed into vector embeddings (typically via Titan Text Embeddings).

**RAG Flow:** When a user asks about fund characteristics, Nova Pro queries the S3-backed index to retrieve relevant text segments to ground its answer.

#### 2. Live Action Group (Lambda & MF APIs)

- **Logic Layer:** A Python-based AWS Lambda function acting as a unified dispatcher for the mfapi.in suite.

**Functionality:**

- **search_fund:** Sanitizes natural language queries (removing filler words like "mutual fund") to retrieve 6-digit AMFI scheme codes.
- **get_latest_nav:** Real-time retrieval of the most recent Net Asset Value and date.
- **get_historical_nav:** Fetches time-series data with a 90-day window limit to ensure low latency.

**The Handshake Fix:** The Lambda is programmed to echo the apiPath and httpMethod sent by Nova Pro, ensuring the Agent validates the response.

#### 3. Amazon Bedrock Agents

- **Core Model:** Amazon Nova Pro serves as the "brain." It was chosen for its strong reasoning capabilities and its ability to handle complex tool-calling sequences.

**Decision Logic:**

1. **Identify:** Nova Pro parses the user intent (e.g., "What is the NAV for the fund in this factsheet?").
2. **Retrieve:** It queries the S3 Knowledge Base to find the specific fund name or AMFI code from the PDF.
3. **Act:** If real-time data is needed, it triggers the Lambda Action Group.
4. **Synthesize:** It combines the PDF's qualitative data with the Lambda's quantitative data into a single formatted Markdown response.

## AWS Services Used

| AWS Service | Key Functionality | Description |
|-------------|-------------------|-------------|
| Amazon Nova Pro | Intelligence & Reasoning | Powers the AI assistant with advanced reasoning capabilities. |
| Bedrock Knowledge Base | Scanning PDF Factsheets (RAG) | Enables retrieval of information from mutual fund fact sheets using vector search. |
| S3 (Managed Vectors) | Storing "AI-ready" document data | Hosts vectorized data for efficient querying and storage. |
| AWS Lambda | Real-time API Integration (NAV/Codes) | Handles dynamic data retrieval for NAV and scheme codes via APIs. |
| IAM | Permission & Access Control | Manages secure access to AWS resources and services. |

## AWS Services Usage 

Followings are the screenshots from the system demonstrating key workflow steps and tools.

- **S3 bucket storing PDF fact sheets.**  
  ![S3 Fact Sheets](images/mf_factsheet_s3.png)

- **Bedrock Knowledge Base configuration overview.**  
  ![Knowledge Base Setup](images/aws_bedrock_kb.png)

- **Knowledge Base test query in Bedrock console.**  
  ![Knowledge Base Console Test](images/aws_bedrock_kb_console_test.png)

- **Knowledge Base test query in Bedrock console.**  
  ![Knowledge Base CLI Test](images/aws_bedrock_kb_cli_test.png)

- **Lambda Action Group configuration view.**  
  ![Lambda Action Group](images/lambda_func_mfactiongroup.png)

- **Lambda test execution output (search fund).**  
  ![Lambda Test](images/lambda_func_mfactiongroup_test01.png)

- **Lambda test execution output (NAV lookup).**  
  ![Lambda NAV Test](images/lambda_func_mfactiongroup_test02.png)

- **CLI interaction (Gist of fund allocation).**  
  ![CLI Output](images/aws_agents.png)

- **Bedrock Agent builder - agent details.**  
  ![Agent Builder - Details](images/aws_agent_build_01.png)

- **Bedrock Agent builder - agent details with action group.**  
  ![Agent Builder - Details](images/aws_agent_build_02.png)

- **Bedrock Agent builder - agent details with knowledge base.**  
  ![Agent Builder - Details](images/aws_agent_build_02.png)

- **Bedrock Agent builder - test response trace.**  
  ![Agent Builder - Test](images/aws_agent_test01.png)

- **Bedrock Agent builder - test response trace.**  
  ![Agent Builder - Test](images/aws_agent_test02.png)

- **Bedrock Agent builder - test response trace.**  
  ![Agent Builder - Test](images/aws_agent_test03.png)

## GitHub Repository
Refer https://github.com/sitaramy/awsbedrocktest/tree/main for python script used to build and test AWS AI Services.

## Conclusion

The successful deployment of your Mutual Fund AI Assistant marks a transition from a simple chatbot to a sophisticated, agentic system. By integrating Amazon Nova Pro with a RAG-based Knowledge Base and real-time Lambda Action Groups, we have built a tool that doesn't just "talk" about finance—it actively researches and calculates data with high precision.
