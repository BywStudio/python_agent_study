# 导入 generate_copy
from xiaohongshuFinal import generate_copy

import re

# 定义测试用例
test_cases = [
    ("降噪耳机", "学生党、高性价比"),
    ("螺蛳粉", "深夜食堂、重口味、懒人速食"),
    ("瑜伽垫", "健身小白、居家运动、便宜好用"),
    ("宝宝辅食", "新手妈妈、营养均衡、简单快手"),
    ("机械键盘", "程序员、客制化、手感至上"),
    ("防晒霜", "敏感肌、夏天必备、平价大碗"),
]

# 定义校验函数 validate，自动检查一条结果是否达标
def validate(copy: dict) -> dict:
    errors = []

    # 1. 基本字段存在
    for key in ["thinking", "title", "content", "tags"]:
        if key not in copy or not copy[key]:
            errors.append(f"缺少或为空: {key}")

    # 2. content 里必须有至少 3 个 emoji
    # emoji 的简单正则（覆盖大部分常见 emoji）
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F300-\U0001F5FF"  # 符号和象形文字
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F1E0-\U0001F1FF"  # 国旗
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE
    )

    if "content" in copy and copy["content"]:
        emojis = emoji_pattern.findall(copy["content"])
        # 简单粗暴的统计字符数
        emoji_count = sum(len(e) for e in emojis)
        if emoji_count < 3:
            errors.append(f"content 中 emoji 数量不足，检测到约 {emoji_count} 个")

    # 3. content 里必须分段（至少一个换行）
    if "content" in copy and "\n" not in copy["content"]:
        errors.append("content 没有换行分段")

    # 4. tags 必须是列表且至少 3 个
    if "tags" in copy:
        if not isinstance(copy["tags"], list) or len(copy["tags"]) < 3:
            errors.append("tags 不是列表或数量不足 3 个")

    return {
        "pass": len(errors) == 0,
        "errors": errors
    }

# 批量测试循环
if __name__ == "__main__":
    passed = 0
    failed = 0

    for product, style in test_cases:
        print(f"\n{'='*40}")
        print(f"测试商品: {product} | 风格: {style}")
        print('=' * 40)

        result = generate_copy(product, style)
        check = validate(result)

        if "error" in result:
            print(f"❌ API/解析失败: {result['error']}")
            failed += 1
            continue

        if check["pass"]:
            print("✅ 通过校验")
            print(f"标题: {result['title']}")
            print(f"标签: {result['tags']}")
            passed += 1
        else:
            print("❌ 未通过校验:")
            for err in check["errors"]:
                print(f"    - {err}")
            failed += 1
    print(f"\n{'=' * 40}")
    print(f"测试完成: 通过 {passed} / 失败 {failed}")

