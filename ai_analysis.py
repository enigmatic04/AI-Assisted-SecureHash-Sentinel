import os
from openai import OpenAI


def analyze_security(data):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "AI analysis is not configured. Please add your OpenAI API key."

    client = OpenAI(api_key=api_key)

    prompt = f"""
You are a cybersecurity assistant analyzing a file integrity event.

File name: {data["filename"]}

Integrity status: {data["status"]}

Hash difference: {data["difference"]}%

Different bits: {data["different_bits"]} out of 256

Risk level: {data["risk"]}

SHA-256 execution time: {data["execution_time"]} seconds


Give a concise security analysis.

Include:

1. What happened
2. Possible reason
3. Recommended action

Do not claim that the file is malicious.
A hash mismatch only indicates that the file contents changed.
"""


    try:
        response = client.responses.create(
            model="gpt-5.6-luna",
            input=prompt
        )

        return response.output_text


    except Exception as error:

        return f"AI analysis failed: {error}"