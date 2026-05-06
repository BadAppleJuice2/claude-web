#!/usr/bin/env python3
"""
SQL生成器
将自然语言描述转换为SQL查询

使用场景:
- 非技术人员查询数据库
- 快速生成复杂SQL
- SQL学习辅助
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deepseek_sdk import DeepSeekClient, ChatSession


# 模拟数据库Schema
SAMPLE_SCHEMA = """
表结构:

users (用户表)
- id: INT PRIMARY KEY
- username: VARCHAR(50)
- email: VARCHAR(100)
- created_at: DATETIME
- status: ENUM('active', 'inactive')

orders (订单表)
- id: INT PRIMARY KEY
- user_id: INT (外键关联users.id)
- total_amount: DECIMAL(10,2)
- status: ENUM('pending', 'paid', 'shipped', 'completed', 'cancelled')
- created_at: DATETIME

products (商品表)
- id: INT PRIMARY KEY
- name: VARCHAR(100)
- price: DECIMAL(10,2)
- stock: INT

order_items (订单明细表)
- id: INT PRIMARY KEY
- order_id: INT (外键关联orders.id)
- product_id: INT (外键关联products.id)
- quantity: INT
- price: DECIMAL(10,2)
"""


def generate_sql(natural_language: str, schema: str = SAMPLE_SCHEMA) -> str:
    """
    将自然语言转换为SQL

    Args:
        natural_language: 自然语言描述
        schema: 数据库Schema

    Returns:
        SQL查询语句
    """
    client = DeepSeekClient()

    system_prompt = f"""你是一位SQL专家。根据提供的数据库Schema，将用户的自然语言描述转换为正确的SQL查询。

{schema}

要求:
1. 只返回SQL语句，不要解释
2. 使用标准SQL语法
3. 添加适当的注释说明查询目的
4. 如果查询涉及多个表，使用JOIN并指定连接条件
5. 考虑性能优化（如使用索引字段）"""

    response = client.chat(
        message=natural_language,
        system_prompt=system_prompt,
        temperature=0.2,
        max_tokens=1000
    )

    return response.content


def explain_sql(sql: str) -> str:
    """解释SQL查询的含义"""
    client = DeepSeekClient()

    prompt = f"请解释以下SQL查询的作用和执行逻辑:\n\n```sql\n{sql}\n```"

    response = client.chat(
        message=prompt,
        system_prompt="你是一位SQL老师，用通俗易懂的语言解释SQL查询",
        temperature=0.5
    )

    return response.content


def interactive_mode():
    """交互式SQL生成模式"""
    print("🗄️  SQL生成器 (输入 'quit' 退出)\n")
    print(f"当前Schema: 电商系统 (users, orders, products, order_items)\n")

    session = ChatSession(
        DeepSeekClient(),
        system_prompt=f"""你是一位SQL专家。根据以下Schema回答用户的SQL相关问题。

{SAMPLE_SCHEMA}

你可以:
1. 根据自然语言生成SQL
2. 解释SQL查询的含义
3. 优化SQL性能
4. 回答SQL相关问题"""
    )

    while True:
        user_input = input("\n💬 你的问题: ").strip()

        if user_input.lower() in ['quit', 'exit', 'q']:
            print("再见!")
            break

        if not user_input:
            continue

        print("\n🤖 生成中...")
        response = session.send(user_input)
        print(f"\n📋 回答:\n{response}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='SQL生成器')
    parser.add_argument('query', nargs='?', help='自然语言查询(可选)')
    parser.add_argument('-i', '--interactive', action='store_true', help='交互模式')
    parser.add_argument('-e', '--explain', help='解释SQL文件')

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()
    elif args.explain:
        with open(args.explain, 'r') as f:
            sql = f.read()
        explanation = explain_sql(sql)
        print(explanation)
    elif args.query:
        sql = generate_sql(args.query)
        print("\n📝 生成的SQL:\n")
        print(sql)
    else:
        # 演示模式
        demo_queries = [
            "查询最近30天内注册的用户数量",
            "找出消费金额最高的前10名用户",
            "统计每个商品类别的总销售额",
            "查询超过7天未发货的订单"
        ]

        print("🗄️  SQL生成器演示\n")

        for query in demo_queries:
            print(f"💬 {query}")
            print("-" * 50)
            sql = generate_sql(query)
            print(f"{sql}\n")


if __name__ == "__main__":
    main()
