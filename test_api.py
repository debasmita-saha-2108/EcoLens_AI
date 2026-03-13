import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
key = os.getenv("GROQ_API_KEY")

if key:
    print(f"✅ Success! Key found: {key[:5]}...{key[-4:]}")
    try:
        client = Groq(api_key=key)
        # Quick test call
        res = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say hello!"}],
            model="llama-3.3-70b-versatile"
        )
        print("🤖 Groq Response:", res.choices[0].message.content)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
else:
    print("❌ Error: GROQ_API_KEY not found in .env file.")