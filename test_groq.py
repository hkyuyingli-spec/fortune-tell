import tomllib

from openai import OpenAI

with open(".streamlit/secrets.toml", "rb") as secrets_file:
    secrets = tomllib.load(secrets_file)

api_key = secrets.get("GROQ_API_KEY")
if not api_key or api_key == "your-key-here":
    raise SystemExit('Set GROQ_API_KEY in .streamlit/secrets.toml before testing.')

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key,
)
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Say hello in one sentence."}],
    max_tokens=50,
)
print(response.choices[0].message.content)
