from validator import validate_test_cases
import json

from llm_client import generate_response


def generate_test_cases(endpoint):

    prompt = f"""
You are an experienced API Automation Test Engineer.

Generate API test scenarios based ONLY on the
following OpenAPI endpoint specification.

Endpoint:
{json.dumps(endpoint, indent=2)}

Generate:
1. Positive test scenarios.
2. Negative test scenarios.
3. Boundary test scenarios, only when applicable.

Return valid JSON only in this format:

{{
    "test_cases": [
        {{
            "test_id": "TC_001",
            "test_type": "Positive",
            "description": "Retrieve a valid user",
            "method": "GET",
            "endpoint": "/users/1",
            "expected_status": 200
        }}
    ]
}}


RULES:

1. Generate test cases ONLY for the supplied endpoint.

2. The exact endpoint path is:
   {endpoint["path"]}

3. The exact HTTP method is:
   {endpoint["method"]}

4. Never add path segments that are not defined
   in the supplied endpoint.

5. If the endpoint is /users, generate /users.
   Never change it to /users/1 or /users/999.

6. If the endpoint contains path parameters such
   as /users/{id}, replace them with concrete values.

7. Generate at least one positive test case.

8. Generate negative cases only when supported
   by the endpoint specification.

9. Generate boundary cases only when applicable
   parameter constraints are documented.

10. Use only documented HTTP response codes.

11. Do not invent application behavior or
    unsupported endpoint paths.

12. Each test case must contain:
    test_id, test_type, description,
    method, endpoint, expected_status.

13. Allowed test types:
    Positive, Negative, Boundary.

14. Return valid JSON only.


DESCRIPTION RULES:

1. The description must accurately reflect
   the endpoint's documented behavior.

2. Use the endpoint summary to understand
   the purpose of the API.

3. For GET /users, describe retrieving
   all users, not a single user.

4. For GET /users/{id}, describe retrieving
   a specific user.

5. For negative tests, clearly describe
   the invalid input or error condition.

6. Do not invent API behavior that is
   absent from the specification.


"""

    response = generate_response(prompt)

    try:
        result = json.loads(response)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"AI returned invalid JSON: {error}"
        )

    if not isinstance(result, dict):
        raise ValueError(
            "AI response must be a JSON object."
        )

    if not isinstance(result.get("test_cases"), list):
        raise ValueError(
            "AI response must contain a test_cases list."
        )

    return result["test_cases"]


if __name__ == "__main__":

    from openapi_parser import (
        load_openapi_spec,
        extract_endpoints
    )

    specification = load_openapi_spec("sample_api.yaml")

    endpoints = extract_endpoints(specification)

    for endpoint in endpoints:

        print(
            f"\nGenerating test cases for "
            f"{endpoint['method']} {endpoint['path']}"
        )


        test_cases = generate_test_cases(endpoint)

        print(
            f"\nAI generated: {len(test_cases)} test cases"
        )

        valid_cases, errors = validate_test_cases(
            test_cases,
            endpoint
        )

        print(
            f"Valid test cases: {len(valid_cases)}"
        )

        print(
            f"Rejected test cases: {len(errors)}"
        )

        print("\nVALID TEST CASES:")

        for test_case in valid_cases:
            print(json.dumps(test_case, indent=2))

        if errors:

            print("\nVALIDATION ERRORS:")

            for error in errors:
                print("-", error)

