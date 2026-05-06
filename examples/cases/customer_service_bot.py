#!/usr/bin/env python3
"""
智能客服机器人
多轮对话，处理常见客户问题

使用场景:
- 网站客服
- 常见问题解答
- 工单预处理
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from deepseek_sdk import DeepSeekClient, ChatSession


# 知识库
KNOWLEDGE_BASE = """
公司信息:
- 名称: 智云科技
- 主营: 云计算服务、AI解决方案
- 工作时间: 周一至周五 9:00-18:00
- 客服电话: 400-123-4567

产品信息:
1. 云服务器ECS
   - 价格: 99元/月起
   - 配置: 1核2G起步
   - 特点: 弹性扩展、按需付费

2. 对象存储OSS
   - 价格: 0.12元/GB/月
   - 特点: 高可靠、CDN加速

3. AI推理服务
   - 价格: 按调用量计费
   - 特点: 预置主流模型、低延迟

常见问题:
Q: 如何退款?
A: 购买7天内可申请退款，联系客服处理

Q: 如何升级配置?
A: 控制台可直接升级，无需停机

Q: 发票怎么开?
A: 控制台申请，电子发票即时开具
"""


class CustomerServiceBot:
    """智能客服机器人"""

    def __init__(self):
        self.client = DeepSeekClient()
        self.session = ChatSession(
            self.client,
            system_prompt=f"""你是一位专业的客服代表。请根据以下知识库回答客户问题。

{KNOWLEDGE_BASE}

服务原则:
1. 态度友好、耐心
2. 回答准确、简洁
3. 不确定的问题引导联系人工客服
4. 主动询问是否解决了问题

如果客户问题在知识库中没有答案，请说:"抱歉，这个问题我需要转接人工客服为您解答，请拨打 400-123-4567 或留言。""""
        )

    def handle_message(self, message: str) -> str:
        """处理用户消息"""
        return self.session.send(message)

    def reset(self):
        """重置对话"""
        self.session.clear()


def run_chatbot():
    """运行客服机器人"""
    print("🤖 智云科技智能客服")
    print("=" * 50)
    print("您好！我是智能客服助手，有什么可以帮您？")
    print("(输入 'quit' 退出, 'reset' 重置对话)")
    print("=" * 50)

    bot = CustomerServiceBot()

    while True:
        try:
            user_input = input("\n👤 客户: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n🤖 客服: 感谢咨询，祝您生活愉快！")
                break

            if user_input.lower() == 'reset':
                bot.reset()
                print("\n🤖 客服: 对话已重置，请问有什么可以帮您？")
                continue

            print("\n🤖 客服: ", end="", flush=True)

            # 流式输出
            response = bot.client.chat(
                message=user_input,
                system_prompt=bot.session.messages[0].content if bot.session.messages else "",
                temperature=0.7
            )

            print(response.content)

        except KeyboardInterrupt:
            print("\n\n再见!")
            break
        except Exception as e:
            print(f"\n❌ 出错了: {e}")


def demo_conversation():
    """演示对话"""
    print("🤖 客服对话演示\n")

    bot = CustomerServiceBot()

    demo_messages = [
        "你好，我想了解一下云服务器",
        "99元的是什么样的配置？",
        "可以升级配置吗？",
        "怎么购买？",
        "谢谢"
    ]

    for msg in demo_messages:
        print(f"👤 客户: {msg}")
        response = bot.handle_message(msg)
        print(f"🤖 客服: {response}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='智能客服机器人')
    parser.add_argument('-d', '--demo', action='store_true', help='演示模式')

    args = parser.parse_args()

    if args.demo:
        demo_conversation()
    else:
        run_chatbot()
