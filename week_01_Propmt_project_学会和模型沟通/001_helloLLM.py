from openai import OpenAI

client = OpenAI(
    api_key = "sk-2fdd2b2a68ff49a89e25dc852a7d41f9",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model = "qwen-plus",
    messages = [
        { "role": "user", "content": "你好, 请用一句话介绍你自己" }
    ]
)

print(response.choices[0].message.content)
