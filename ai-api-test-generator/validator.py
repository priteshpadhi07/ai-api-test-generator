
import re


ALLOWED_TYPES = {"Positive", "Negative", "Boundary"}

REQUIRED_FIELDS = [
    "test_id",
    "test_type",
    "description",
    "method",
    "endpoint",
    "expected_status"
]


def validate_test_cases(test_cases, endpoint):

    valid_cases = []
    errors = []

    method = endpoint["method"]
    path = endpoint["path"]

    documented_statuses = {
        int(status)
        for status in endpoint["responses"]
        if str(status).isdigit()
    }

    # Convert /users/{id} into a regex accepting
    # a single concrete path segment.
    path_pattern = re.escape(path)

    path_pattern = re.sub(
        r"\\\{[^{}]+\\\}",
        r"[^/]+",
        path_pattern
    )

    path_pattern = "^" + path_pattern + "$"

    seen = set()

    for index, case in enumerate(test_cases, start=1):

        if not isinstance(case, dict):
            errors.append(f"Case {index}: Not a JSON object")
            continue

        missing = [
            field for field in REQUIRED_FIELDS
            if field not in case
        ]

        if missing:
            errors.append(
                f"Case {index}: Missing fields {missing}"
            )
            continue

        if case["test_type"] not in ALLOWED_TYPES:
            errors.append(
                f"Case {index}: Invalid test type"
            )
            continue

        if case["method"] != method:
            errors.append(
                f"Case {index}: HTTP method mismatch"
            )
            continue

        if not isinstance(case["endpoint"], str) or not re.fullmatch(
            path_pattern, case["endpoint"]
        ):
            errors.append(
                f"Case {index}: Endpoint path mismatch"
            )
            continue

        if (
            type(case["expected_status"]) is not int
            or case["expected_status"] not in documented_statuses
        ):
            errors.append(
                f"Case {index}: Undocumented status code"
            )
            continue

        if (
            not isinstance(case["test_id"], str)
            or not case["test_id"].strip()
            or not isinstance(case["description"], str)
            or not case["description"].strip()
        ):
            errors.append(
                f"Case {index}: Invalid ID or description"
            )
            continue

        # Semantic validation of test classifications

        test_type = case["test_type"]
        expected_status = case["expected_status"]

        if test_type == "Positive":

            if not 200 <= expected_status < 300:
                errors.append(
                    f"Case {index}: Positive test must "
                    "expect a 2xx response"
                )
                continue

        elif test_type == "Negative":

            if not 400 <= expected_status < 500:
                errors.append(
                    f"Case {index}: Negative test must "
                    "expect a 4xx response"
                )
                continue

        elif test_type == "Boundary":

            parameters = endpoint.get("parameters", [])

            has_constraints = any(
                isinstance(param, dict)
                and isinstance(param.get("schema"), dict)
                and any(
                    key in param["schema"]
                    for key in [
                        "minimum",
                        "maximum",
                        "minLength",
                        "maxLength",
                        "minItems",
                        "maxItems"
                    ]
                )
                for param in parameters
            )

            if not has_constraints:
                errors.append(
                    f"Case {index}: Boundary test has "
                    "no documented parameter constraints"
                )
                continue

        # Prevent exact duplicate test cases
        key = (
            case["method"],
            case["endpoint"],
            case["expected_status"]
        )

        if key in seen:
            errors.append(
                f"Case {index}: Duplicate test case"
            )
            continue

        seen.add(key)
        valid_cases.append(case)

    return valid_cases, errors
