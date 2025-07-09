# deepseek_adapter.py
"""
CrewAI与DeepSeek模型兼容性适配器

该模块提供了一个自定义的LLM（大语言模型）类，作为CrewAI框架和
任何兼容OpenAI接口但可能不支持所有高级参数的LLM（如DeepSeek）之间的桥梁。

核心问题：
CrewAI在内部调用其LLM时，会传递一些框架特有的、用于状态跟踪和回调的参数
（例如 'callbacks', 'from_task', 'from_agent'）。如果目标LLM的SDK
（如此处的 'langchain-openai'）不能识别这些参数，就会导致程序崩溃。

解决方案：
`CrewAIFallbackLLM` 类继承自 `crewai.llm.LLM`，并重写了 `call` 方法。
它在将请求转发给实际的LLM实例之前，会从关键字参数（`kwargs`）中
安全地移除所有已知的不兼容参数。这确保了只有纯净、兼容的请求被发送出去，
从而解决了兼容性问题，使得在CrewAI中使用DeepSeek等模型成为可能。
"""

from crewai.llm import LLM
from typing import Any, cast

class CrewAIFallbackLLM(LLM):
    """
    一个自定义LLM类，用于强制CrewAI使用更通用的方式调用LLM。
    它接收一个可以工作的langchain LLM实例，并确保在调用时只传递最核心的prompt，
    避免CrewAI加入可能导致不兼容的额外参数。
    """
    llm: Any

    def __init__(self, llm_instance: Any):
        """
        初始化适配器。
        
        参数:
            llm_instance: 一个已经实例化的、可以工作的Langchain LLM对象。
        """
        super().__init__(model=llm_instance.model_name)
        self.llm = llm_instance

    def call(self, prompt: str, **kwargs: Any) -> str:
        """
        重写的调用方法，在转发请求前过滤不兼容的参数。
        """
        # 关键修正：从kwargs中安全地移除所有已知的不兼容键。
        kwargs.pop('callbacks', None)
        kwargs.pop('from_task', None)
        kwargs.pop('from_agent', None)

        # 核心逻辑：调用原始的llm实例
        response = self.llm.invoke(prompt, **kwargs)
        return cast(str, response.content)

    @property
    def _llm_type(self) -> str:
        """让CrewAI知道这是一个自定义的LLM"""
        return "custom_deepseek_adapter" 