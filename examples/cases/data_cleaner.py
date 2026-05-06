#!/usr/bin/env python3
"""
数据清洗助手
自动识别并清洗脏数据

使用场景:
- 数据预处理
- 数据质量检查
- ETL流程
"""

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deepseek_sdk import DeepSeekClient


def analyze_data(file_path: str, sample_size: int = 20) -> dict:
    """分析数据文件，提取样本"""
    ext = Path(file_path).suffix.lower()
    sample = []

    try:
        if ext == '.csv':
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                for i, row in enumerate(reader):
                    if i >= sample_size:
                        break
                    sample.append(row)
            return {"type": "csv", "headers": headers, "sample": sample}

        elif ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    sample = data[:sample_size]
                else:
                    sample = [data]
            return {"type": "json", "sample": sample}

        else:
            # 文本文件
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()[:sample_size]
            return {"type": "text", "sample": lines}

    except Exception as e:
        return {"error": str(e)}


def generate_cleaning_plan(data_info: dict) -> str:
    """使用AI生成数据清洗方案"""
    client = DeepSeekClient()

    system_prompt = """你是一位数据工程师。请分析提供的数据样本，生成数据清洗方案。

方案应包含:
1. 数据质量问题识别
2. 具体的清洗步骤
3. Python代码实现
4. 质量检查建议"""

    content = f"""请为以下数据生成清洗方案:

数据类型: {data_info.get('type', 'unknown')}
样本数据:
```
{json.dumps(data_info, ensure_ascii=False, indent=2)[:3000]}
```
"""

    response = client.chat(
        message=content,
        system_prompt=system_prompt,
        temperature=0.3,
        max_tokens=2500
    )

    return response.content


def main():
    import argparse

    parser = argparse.ArgumentParser(description='数据清洗助手')
    parser.add_argument('file', help='数据文件路径')
    parser.add_argument('-n', '--sample', type=int, default=20, help='样本行数')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"错误: 文件不存在 {args.file}")
        return

    print(f"📁 正在分析数据: {args.file}\n")

    # 分析数据
    data_info = analyze_data(args.file, args.sample)

    if "error" in data_info:
        print(f"❌ 分析失败: {data_info['error']}")
        return

    print(f"✅ 数据类型: {data_info['type']}")
    if 'headers' in data_info:
        print(f"   字段: {', '.join(data_info['headers'])}")
    print(f"   样本数: {len(data_info['sample'])}\n")

    # 生成清洗方案
    print("🤖 正在生成清洗方案...\n")
    plan = generate_cleaning_plan(data_info)

    print("=" * 60)
    print("📋 数据清洗方案")
    print("=" * 60)
    print(plan)


if __name__ == "__main__":
    main()
