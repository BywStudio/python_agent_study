"""
现在每次生成文案，都要重复写一大段代码:
1. 定义 client
2. 写 system
3. 写 user
4. 调用 API
5. 解析 JSON

函数就是把这些重复的步骤打包成一个功能，只需要扔进去两个东西:
- product: 产品名
- syle: 风格词
"""

import json
from openai import OpenAI

"""
为什么把 client 放在外面?
- client 只需要创建一次，不用每次调用都生成一次
- 如果放在函数里面，每次调用函数都新建一个 client，浪费资源
"""
client = OpenAI(
    api_key = "sk-2fdd2b2a68ff49a89e25dc852a7d41f9",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

"""
def: 
    - defile 缩写, 表示我要创造一个函数【就像说: 我要发明一个机器】
generate_copy: 
    - 函数的名字，自己取的【机器的名字】
(product: str, style: str): 
    - 函数的入口参数【机器的进料口】
-> dict: 
    - 函数的返回类型提示【机器的出料口，提示这里会吐出一个字典】
pass: 一个占位符，表示这里先空着，晚点再填
"""
def generate_copy(product: str, style: str) -> dict:
    # 把整套 API 调用塞进函数
    user_prompt = f"""请为"{product}"写一篇小红书风格的种草文案。
    【风格要求】{style}
    【输出格式】请直接输出 JSON，格式如下:
    {{"title": "标题", "content": "正文内容"}}
    """
    response = client.chat.completions.create(
        model = "qwen-plus",
        messages = [
            { "role": "user", "content": user_prompt }
        ]
    )

    # 把 JSON 解析也塞进函数
    raw = response.choices[0].message.content.strip()
    # 防御性编程: 如果模型不通话，包一层 ```json ...```
    if raw.startswith("```"):
        raw = raw.strip("`").replace("json", "").strip()

    result = json.loads(raw)
    return result

# 调用函数来测试
if __name__ == "__main__":
    print("=== 生成第一个文案 ===")
    copy1 = generate_copy("降噪耳机", "学生党、高性价比、沉浸式")
    print("标题: ", copy1["title"])
    print("正文: ", copy1["content"])

    print("\n=== 生成第二个文案 ===")
    copy2 = generate_copy("便携式榨汁杯", "健身、办公、懒人必备")
    print("标题", copy2["title"])
    print("正文", copy2["content"])
