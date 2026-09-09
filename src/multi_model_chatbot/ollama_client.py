from ollama import chat


def generate_response(model, messages):
    response = chat(
        model=model,
        messages=messages,
        stream=True,
    )

    for chunk in response:
        content = chunk.message.content

        if content:
            yield content