# 1. 基本格式
import json
from openai import OpenAI

client = OpenAI(
    api_key = "sk-2fdd2b2a68ff49a89e25dc852a7d41f9",
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# 2. system propmt
system_prompt = """你是一位深谙小红书平台算法的顶级爆款文案写手。你的任务是根据用户提供的商品和风格，创作具有强烈网感、高传播欲的小红书种草文案。
【创作风格要求】
1. 语言必须口语化、网络化，熟练使用"家人们"、"真的绝了"、"谁懂啊"、"挖到宝了"、"闭眼入" 等小红书高频词汇
2. 正文必须分段，结构清晰：痛点引入 -> 产品亮点 -> 使用场景 -> 结尾号召
3. 必须大量使用 emoji 点缀，增强视觉冲击力
4. 标题控制在 25 字以内，必须包含 emoji

【输出格式要求】
你必须直接输出合法的 JSON，不要添加 markdown 代码块标记，不要添加任何解释性文字，格式如下:
{
    "thinking": "你的思维链分析过程...",
    "title": "...",
    "content": "...",
    "tags": ["...", "..."]
}

【思考过程 thinking 要求】
在生成文案钱，你必须现在 thinking 字段中完成以下三步分析:
1. 目标人群画像: 谁最可能买这个商品? ta 的核心痛点是什么
2. 卖点提炼: 这个产品最能打动 ta 的 2-3 个量点是什么?
3. 网感设计: 要用什么口吻、emoji 组合、钩子话术来抓住眼球?
"""

# 上面的 system propmt 还可以添加一些输出的示例，如之前的学生党耳机等

# 3. generate_copy 
"""
函数内的逻辑:
1. 用 f-string 组装 user_prompt，告诉模型商品和风格
2. 调用 client.chat.completions.create(), 注意这次要把 system_prompt 放进去
3. 解析 JSON
4. 返回字典
"""
def generate_copy(product: str, style: str) -> dict:
    try:
        user_prompt = f"""请为商品【{product}】创作一片小红书文案。
        【风格要求】{style}
        请严格按照 system_prompt 中的格式输出 JSON，包含 thinking、title、content、tags四个字段
        """
        response = client.chat.completions.create(
            model = "qwen-plus",
            messages = [
                { "role": "system", "content": system_prompt },
                { "role": "user","content": user_prompt }
            ],
            # 稍微放开一点创造性，0.7 比默认更活泼
            temperature = 0.7
        )
        # 处理 JSON
        raw = response.choices[0].message.content.strip()

        # 防御性清晰（模型偶尔不听话）
        if raw.startswith("```"):
            raw = raw.strip("`").replace("json", "").strip()

        result = json.loads(raw)

        # 字段校验
        required_keys = ["thinking", "title", "content", "tags"]
        for key in required_keys:
            if key not in required_keys:
                raise ValueError(f"返回结果缺少必要字段: {key}")

        # 额外校验: tags 必须是列表
        if not isinstance(result["tags"], list):
            raise ValueError("tags 必须是列表格式")

        return result
    
    except Exception as e:
        print(f"[错误] 生成 {product} 时失败: {e}")
        return {
            "error": str(e),
            "thinking": "",
            "title": "",
            "content": "",
            "tags": []
        }

# 4. 增加健壮性（try + except + 字段校验）
# 把上面的函数用 try-except 包裹起来，并校验返回的字段


# 5. main 测试块
if __name__ == "__main__":
    print("=== 测试: 降噪耳机 ===")
    copy = generate_copy("降噪耳机", "学生党、高性价比、沉浸式")

    if "error" not in copy:
        print(f"思考过程: \n{copy['thinking']}\n")
        print(f"标题: {copy['title']}\n")
        print(f"正文: \n{copy['content']}\n")
        print(f"标签: {copy['tags']}")
    else:
        print("生成失败，请检查报错信息")

