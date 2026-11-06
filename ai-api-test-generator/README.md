# AI-Powered API Test Generator

An AI-assisted API automation testing framework built using Python, Ollama (Llama 3.2), OpenAPI specifications, and Requests.

## Features

- Parse OpenAPI YAML and JSON specifications.
- Extract API endpoints, methods, parameters, and documented response codes.
- Generate positive, negative, and boundary test candidates using local AI.
- Validate AI-generated test cases before execution.
- Reject unsupported HTTP methods, invalid endpoint paths, undocumented status codes, and duplicate scenarios.
- Execute validated GET API test cases using Python Requests.
- Compare expected and actual HTTP status codes.
- Capture API response times.
- Generate formatted Excel test execution reports.

## Technologies Used

- Python
- Ollama
- Llama 3.2
- Requests
- PyYAML
- OpenPyXL

## Project Structure

```text
ai-api-test-generator/
│
├── main.py
├── llm_client.py
├── openapi_parser.py
├── ai_test_generator.py
├── validator.py
├── api_executor.py
├── report_generator.py
├── sample_api.yaml
├── requirements.txt
└── README.md
```

## How It Works

1. Read the OpenAPI specification.
2. Extract API endpoint details.
3. Generate test cases using Llama 3.2.
4. Validate the generated test cases.
5. Reject invalid test cases.
6. Execute supported API requests.
7. Compare expected and actual results.
8. Export results to Excel.

## Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

Install Ollama and download the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Ensure Ollama is running locally.

## Run the Project

```bash
python main.py
```

The application uses `sample_api.yaml` and executes supported GET requests against the configured JSONPlaceholder sample API.

## Sample Execution Results

| Test ID | Endpoint | Expected | Actual | Result |
|---|---|---|---|---|
| TC_001 | /users | 200 | 200 | PASS |
| TC_002 | /users/1 | 200 | 200 | PASS |
| TC_003 | /users/0 | 404 | 404 | PASS |

These are sample results from one execution. AI-generated scenarios and actual responses may vary.

## Excel Report

The application generates:

`AI_API_Test_Report.xlsx`

The report includes test IDs, descriptions, HTTP methods, endpoints, expected status codes, actual status codes, execution results, response times, and error messages.

## Current Limitations

- Automated execution is restricted to GET requests against the approved sample API.
- Validation checks basic structure and selected semantic rules, but does not fully verify API behavior or parameter boundaries.
- Authentication, custom headers, request bodies, and response-schema assertions are not yet implemented.
- AI-generated test cases require validation and may still contain incorrect assumptions.

## Future Enhancements

- Support POST, PUT, PATCH, and DELETE requests.
- Add response body and JSON schema validation.
- Support authentication and custom headers.
- Improve parameter and boundary validation.
- Integrate pytest and Jenkins CI/CD.
