
import requests


def generate_response(prompt):

    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2
        }
    }

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=300
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Unable to connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "Ollama request timed out."
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"Ollama API error: {error}"
        )

    except (KeyError, ValueError) as error:
        raise RuntimeError(
            f"Invalid Ollama response: {error}"
        )


if __name__ == "__main__":

    prompt = """
    Return valid JSON only:

    {
        "status": "success",
        "message": "Ollama connection successful"
    }
    """

    response = generate_response(prompt)

    print("\nOllama Response:")
    print(response)
