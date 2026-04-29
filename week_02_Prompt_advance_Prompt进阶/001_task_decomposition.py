import json
from openai import OpenAI

client = OpenAI(
    api_key = "sk-2fdd2b2a68ff49a89e25dc852a7d41f9",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 准备测试数据
POEM = """
《静夜思》
作者：李白
床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。
""".strip()

# 写无步骤版本
def analyze_without_steps(poem: str) -> str:
    # 不给步骤，让模型自由发挥
    system_prompt = "你是一位文学分析师，情分析用户提供的古诗。"
    user_prompt = f"请分析以下这首古诗: \n\n{poem}"

    response = client.chat.completions.create(
        model = "qwen-plus",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0.3
    )

    return response.choices[0].message.content.strip()

# 写有步骤的版本
def analyze_with_steps(poem: str) -> str:
    # 给明确步骤，让模型按步骤分析
    system_prompt = """你是一位专业的中国文学分析师。
【必须严格执行的四个步骤】
第一步: 逐句翻译
- 将古诗的每一句翻译成通俗易懂的白话文

第二步: 意象分析
- 找出诗中出现的核心意象（如: 月亮、霜等）
- 解释每个意象在中国固定文学中常代表什么意义

第三步: 情感解读
- 分析诗人表达了怎样的情感
- 指出通过那些协作手法来传达这种感情

第四步: 一句话总结
- 用一句话概括这首诗的核心主题

【输出格式要求】
- 必须严格按照第一步 -> 第二步 -> 第三步 -> 第四步的顺序输出
- 每个步骤都必须有实质性内容，不能只写标题
"""
    user_prompt = f"请按上述步骤分析一下这首古诗:"
    response = client.chat.completions.create(
        model = "qwen-plus",
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature = 0.3
    )

    return response.choices[0].message.content.strip()

# main 测试块
if __name__ == "__main__":
    print("=" * 60)
    print(f"📜 测试古诗：\n{POEM}\n")
    
    # 版本 A: 无步骤
    print("🔴 版本 A：无步骤分解")
    print("-" * 40)
    result_a = analyze_without_steps(POEM)
    print(result_a)

    # 版本 B: 有步骤
    print("\n🟢 版本 B：有步骤分解")
    print("-" * 40)
    result_b = analyze_without_steps(POEM)
    print(result_b)
