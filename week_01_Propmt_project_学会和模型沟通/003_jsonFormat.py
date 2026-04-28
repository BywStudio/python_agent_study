import json
from openai import OpenAI

client = OpenAI(
    api_key = "sk-2fdd2b2a68ff49a89e25dc852a7d41f9",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# System 角色: 设定人设
system_prompt = "你是一位顶尖的小红书爆款文案写手，你必须直接输出 JSON, 不要添加任何解释"

# User 角色: 用户的具体任务
user_prompt = '请为 "降噪蓝牙耳机" 写一篇文案, 按此 JSON 格式返回: { "title": "...", "content": "..." }'

response = client.chat.completions.create(
    model = "qwen-plus",
    messages = [
        { "role": "system","content": system_prompt},
        { "role": "user", "content": user_prompt}
    ]
)

# 接收输出
raw = response.choices[0].message.content

if raw.startswith("```"):
    raw = raw.strip("`").replace("json", "").strip()

# 字符串 -> 字典
result = json.loads(raw)

print("标题", result["title"])
print("正文", result["content"])
print("数据类型", type(result))
