
import time
import requests


def execute_test_case(test_case, base_url):

    method = test_case["method"]
    endpoint = test_case["endpoint"]
    expected_status = test_case["expected_status"]

    url = base_url.rstrip("/") + endpoint

    result = {
        "test_id": test_case["test_id"],
        "description": test_case["description"],
        "method": method,
        "endpoint": endpoint,
        "expected_status": expected_status,
        "actual_status": None,
        "result": "ERROR",
        "response_time": None,
        "error_message": ""
    }

    start_time = time.perf_counter()

    try:

        response = requests.request(
            method=method,
            url=url,
            timeout=15
        )

        elapsed_time = time.perf_counter() - start_time

        result["actual_status"] = response.status_code
        result["response_time"] = round(
            elapsed_time, 3
        )

        if response.status_code == expected_status:
            result["result"] = "PASS"
        else:
            result["result"] = "FAIL"

    except requests.exceptions.RequestException as error:

        elapsed_time = time.perf_counter() - start_time

        result["response_time"] = round(
            elapsed_time, 3
        )

        result["error_message"] = str(error)

    return result


if __name__ == "__main__":

    sample_test_case = {
        "test_id": "TC_001",
        "description": "Retrieve all users",
        "method": "GET",
        "endpoint": "/users",
        "expected_status": 200
    }

    base_url = "https://jsonplaceholder.typicode.com"

    result = execute_test_case(
        sample_test_case,
        base_url
    )

    for key, value in result.items():
        print(f"{key}: {value}")
