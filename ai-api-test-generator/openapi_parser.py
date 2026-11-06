
import json
import yaml
from pathlib import Path


def load_openapi_spec(file_path):

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(
            f"OpenAPI file not found: {file_path}"
        )

    with open(path, "r", encoding="utf-8") as file:

        if path.suffix.lower() in [".yaml", ".yml"]:
            specification = yaml.safe_load(file)

        elif path.suffix.lower() == ".json":
            specification = json.load(file)

        else:
            raise ValueError(
                "Only JSON and YAML files are supported."
            )

    if not isinstance(specification, dict):
        raise ValueError("Invalid OpenAPI specification.")

    if "openapi" not in specification and "swagger" not in specification:
        raise ValueError(
            "Missing OpenAPI or Swagger version."
        )

    if not isinstance(specification.get("paths"), dict):
        raise ValueError(
            "Missing or invalid paths section."
        )

    return specification


def extract_endpoints(specification):

    endpoints = []

    http_methods = {
        "get", "post", "put", "patch",
        "delete", "head", "options", "trace"
    }

    for path, path_details in specification["paths"].items():

        if not isinstance(path_details, dict):
            continue

        common_parameters = path_details.get("parameters", [])

        for method, details in path_details.items():

            if method.lower() not in http_methods:
                continue

            if not isinstance(details, dict):
                continue

            endpoint = {
                "path": path,
                "method": method.upper(),
                "summary": details.get("summary", ""),
                "parameters": (
                    common_parameters
                    + details.get("parameters", [])
                ),
                "request_body": details.get("requestBody", {}),
                "responses": details.get("responses", {})
            }

            endpoints.append(endpoint)

    return endpoints


if __name__ == "__main__":

    file_path = input(
        "Enter OpenAPI JSON/YAML file path: "
    ).strip().strip('"')

    try:
        specification = load_openapi_spec(file_path)

        endpoints = extract_endpoints(specification)

        print(f"\nTotal endpoints found: {len(endpoints)}")

        for endpoint in endpoints:

            print(
                f"{endpoint['method']} "
                f"{endpoint['path']}"
            )

    except Exception as error:
        print(f"\nERROR: {error}")
