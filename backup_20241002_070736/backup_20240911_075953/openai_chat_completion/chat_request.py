import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def send_openai_request(prompt: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        return content
    except Exception as e:
        return f"Error: {str(e)}"

def test_openai_integration():
    try:
        response = send_openai_request("Hello, can you hear me?")
        return f"OpenAI API test successful. Response: {response}"
    except Exception as e:
        return f"OpenAI API test failed. Error: {str(e)}"
