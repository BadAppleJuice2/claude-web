#!/usr/bin/env python3
"""
DeepSeek Python SDK
简化 DeepSeek API 调用的封装库

使用示例:
    >>> from deepseek_sdk import DeepSeekClient
    >>> client = DeepSeekClient(api_key="sk-xxx")
    >>> print(client.chat("你好").content)
"""

import os
import json
import requests
from typing import List, Dict, Optional, Generator, Union
from dataclasses import dataclass
from enum import Enum


class Model(Enum):
    """DeepSeek 可用模型"""
    CHAT = "deepseek-chat"           # 通用对话模型（速度快）
    REASONER = "deepseek-reasoner"   # 推理模型（复杂任务）


@dataclass
class Message:
    """消息数据类"""
    role: str       # system, user, assistant
    content: str    # 消息内容


@dataclass
class ChatResponse:
    """聊天响应数据类"""
    content: str            # 回复内容
    model: str              # 使用的模型
    usage: Dict             # Token 用量
    finish_reason: str      # 结束原因


class DeepSeekClient:
    """
    DeepSeek API 客户端

    使用示例:
        >>> client = DeepSeekClient(api_key="sk-xxx")
        >>> response = client.chat("你好")
        >>> print(response.content)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "https://api.deepseek.com",
        timeout: int = 60
    ):
        """
        初始化客户端

        Args:
            api_key: API Key，默认从环境变量 DEEPSEEK_API_KEY 读取
            base_url: API 基础 URL
            timeout: 请求超时时间（秒）
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API Key 不能为空，请设置 DEEPSEEK_API_KEY 环境变量或直接传入 api_key 参数"
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def chat(
        self,
        message: Union[str, List[Message]],
        model: Union[Model, str] = Model.CHAT,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        stream: bool = False,
        system_prompt: Optional[str] = None
    ) -> Union[ChatResponse, Generator[str, None, None]]:
        """
        发送聊天请求

        Args:
            message: 用户消息（字符串）或消息列表
            model: 模型名称，默认 deepseek-chat
            temperature: 随机性控制 (0-2)，越低越确定
            max_tokens: 最大生成 token 数
            stream: 是否启用流式输出
            system_prompt: 系统提示词

        Returns:
            ChatResponse 对象，或流式输出的 token 生成器
        """
        # 构建消息列表
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        if isinstance(message, str):
            messages.append({"role": "user", "content": message})
        else:
            messages.extend([{"role": m.role, "content": m.content} for m in message])

        model_name = model.value if isinstance(model, Model) else model

        data = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": stream
        }

        response = self.session.post(
            f"{self.base_url}/chat/completions",
            json=data,
            timeout=self.timeout,
            stream=stream
        )
        response.raise_for_status()

        if stream:
            return self._handle_stream(response)
        else:
            return self._handle_response(response.json())

    def _handle_response(self, data: Dict) -> ChatResponse:
        """处理普通响应"""
        choice = data["choices"][0]
        return ChatResponse(
            content=choice["message"]["content"],
            model=data["model"],
            usage=data.get("usage", {}),
            finish_reason=choice.get("finish_reason", "")
        )

    def _handle_stream(self, response) -> Generator[str, None, None]:
        """处理流式响应，逐 token 返回"""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    json_str = line[6:]
                    if json_str == '[DONE]':
                        break
                    try:
                        chunk = json.loads(json_str)
                        if 'choices' in chunk and chunk['choices']:
                            delta = chunk['choices'][0].get('delta', {})
                            if 'content' in delta:
                                yield delta['content']
                    except json.JSONDecodeError:
                        continue

    def list_models(self) -> List[Dict]:
        """获取可用模型列表"""
        response = self.session.get(f"{self.base_url}/models", timeout=self.timeout)
        response.raise_for_status()
        return response.json().get("data", [])

    def validate_key(self) -> bool:
        """验证 API Key 是否有效"""
        try:
            self.list_models()
            return True
        except requests.exceptions.HTTPError:
            return False


class ChatSession:
    """
    对话会话管理器
    自动维护多轮对话上下文

    使用示例:
        >>> session = ChatSession(client, system_prompt="你是 Python 专家")
        >>> session.send("什么是装饰器？")
        >>> session.send("能给个例子吗？")  # 自动携带上下文
    """

    def __init__(
        self,
        client: DeepSeekClient,
        model: Union[Model, str] = Model.CHAT,
        system_prompt: Optional[str] = None
    ):
        self.client = client
        self.model = model
        self.messages: List[Message] = []

        if system_prompt:
            self.messages.append(Message("system", system_prompt))

    def send(self, message: str, **kwargs) -> str:
        """
        发送消息并获取回复

        Args:
            message: 用户消息
            **kwargs: 传递给 chat() 的额外参数

        Returns:
            AI 回复内容
        """
        self.messages.append(Message("user", message))

        response = self.client.chat(
            message=self.messages,
            model=self.model,
            **kwargs
        )

        self.messages.append(Message("assistant", response.content))
        return response.content

    def clear(self, keep_system: bool = True):
        """清空对话历史"""
        if keep_system and self.messages and self.messages[0].role == "system":
            self.messages = [self.messages[0]]
        else:
            self.messages = []

    def get_history(self) -> List[Message]:
        """获取对话历史"""
        return self.messages.copy()


def quick_chat(message: str, api_key: Optional[str] = None, model: str = "deepseek-chat", **kwargs) -> str:
    """
    快速发起单次对话（便捷函数）

    Args:
        message: 用户消息
        api_key: API Key（默认从环境变量读取）
        model: 模型名称
        **kwargs: 其他参数

    Returns:
        AI 回复内容

    示例:
        >>> from deepseek_sdk import quick_chat
        >>> print(quick_chat("你好"))
    """
    client = DeepSeekClient(api_key=api_key)
    response = client.chat(message, model=model, **kwargs)
    return response.content


if __name__ == "__main__":
    import sys
    message = sys.argv[1] if len(sys.argv) > 1 else "你好，请介绍一下 DeepSeek"
    print(f"用户: {message}\n")
    print("AI: ", end="", flush=True)
    client = DeepSeekClient()
    for token in client.chat(message, stream=True):
        print(token, end="", flush=True)
    print()
