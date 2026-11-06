from report_generator import generate_excel_report
from openapi_parser import (
    load_openapi_spec,
    extract_endpoints
)

from ai_test_generator import generate_test_cases
from validator import validate_test_cases
from api_executor import execute_test_case


def main():

    print("\n===================================")
    print("     AI API TEST GENERATOR")
    print("===================================")

    specification = load_openapi_spec(
        "sample_api.yaml"
    )

    endpoints = extract_endpoints(specification)

    servers = specification.get("servers", [])

    if not servers or not servers[0].get("url"):
        raise ValueError(
            "No API base URL defined in OpenAPI specification."
        )

    base_url = servers[0]["url"]

    # Safety: this version executes GET requests only.
    # The target is our approved sample API.
    if base_url.rstrip("/") != (
        "https://jsonplaceholder.typicode.com"
    ):
        raise ValueError(
            "Unexpected API base URL. "
            "Only the configured sample API is allowed."
        )

    print(f"\nBase URL: {base_url}")
    print(f"Total endpoints: {len(endpoints)}")

    all_results = []

    for endpoint in endpoints:

        print(
            f"\nGenerating test cases for "
            f"{endpoint['method']} {endpoint['path']}"
        )

        if endpoint["method"] != "GET":
            print("Skipped: only GET is supported.")
            continue

        # Step 1: AI test generation
        test_cases = generate_test_cases(endpoint)

        print(
            f"AI generated: {len(test_cases)} test cases"
        )

        # Step 2: Validation
        valid_cases, errors = validate_test_cases(
            test_cases,
            endpoint
        )

        print(f"Valid cases: {len(valid_cases)}")
        print(f"Rejected cases: {len(errors)}")

        for error in errors:
            print("Validation error:", error)

        # Step 3: Execute valid API test cases
        for test_case in valid_cases:

            # Assign a unique ID across all endpoints
            test_case["test_id"] = (
                f"TC_{len(all_results) + 1:03d}"
            )

            print(
                f"\nExecuting {test_case['test_id']} "
                f"{test_case['method']} "
                f"{test_case['endpoint']}"
            )

            result = execute_test_case(
                test_case,
                base_url
            )

            all_results.append(result)

            print(
                f"Expected: {result['expected_status']} | "
                f"Actual: {result['actual_status']} | "
                f"Result: {result['result']}"
            )

    # Step 4: Execution summary
    passed = sum(
        1 for result in all_results
        if result["result"] == "PASS"
    )

    failed = sum(
        1 for result in all_results
        if result["result"] == "FAIL"
    )

    errors = sum(
        1 for result in all_results
        if result["result"] == "ERROR"
    )

    print("\n===================================")
    print("        EXECUTION SUMMARY")
    print("===================================")

    print(f"Total Executed: {len(all_results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors: {errors}")
    generate_excel_report(all_results)


if __name__ == "__main__":
    main()
