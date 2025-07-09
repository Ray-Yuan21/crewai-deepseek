# CrewAI DeepSeek Compatibility Patch

This project provides a simple yet effective compatibility patch that allows you to use DeepSeek models (and other non-natively supported OpenAI-compatible models) within the [CrewAI](https://github.com/joaomdmoura/crewAI) framework.

---

## The Problem

CrewAI is an innovative framework for building multi-agent systems. While it's designed to be flexible, its internal mechanics sometimes pass framework-specific parameters (e.g., `callbacks`, `from_task`, `from_agent`) when calling the Large Language Model (LLM).

When using LLM providers that are not officially and fully supported, like DeepSeek, their client libraries (e.g., `langchain-openai` used with a custom `base_url`) may not recognize these extra parameters. This leads to `TypeError` exceptions, crashing the agent execution, such as:

- `TypeError: Completions.create() got an unexpected keyword argument 'from_task'`
- `TypeError: Completions.create() got an unexpected keyword argument 'from_agent'`
- `TypeError: ... got multiple values for keyword argument 'callbacks'`

## The Solution

This patch introduces a lightweight adapter class, `CrewAIFallbackLLM`, that acts as a bridge between CrewAI and the underlying LLM client.

It works by intercepting the call from CrewAI and sanitizing the keyword arguments (`kwargs`), removing all known incompatible parameters before forwarding the "clean" request to the actual LLM instance. This ensures smooth communication and allows you to leverage the power of DeepSeek within your CrewAI agents.

---

## How to Use

1.  **Copy Files**: Copy the `deepseek_adapter.py` file into your project.
2.  **Install Dependencies**: Make sure you have the required packages installed.
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure API Key**: Create a file named `.env` in your project root and add your DeepSeek API key like this:
    
    ```
    # .env
    DEEPSEEK_API_KEY="your_deepseek_api_key_here"
    ```

4.  **Run the Example**:
    ```bash
    python example.py
    ```

5.  **Implement in Your Code**: In your main script, instead of passing the `ChatOpenAI` instance directly to your agent, wrap it with our adapter. See the `example.py` file for a complete demonstration.

---
---

# CrewAI DeepSeek 兼容性补丁

本项目提供了一个简单而有效的兼容性补丁，它能让你在 [CrewAI](https://github.com/joaomdmoura/crewAI) 框架中使用 DeepSeek 模型（或其他非原生支持的、兼容OpenAI接口的模型）。

---

## 问题所在

CrewAI 是一个用于构建多智能体系统的创新框架。尽管它的设计很灵活，但其内部机制在调用大语言模型（LLM）时，有时会传递一些框架特有的参数（例如 `callbacks`, `from_task`, `from_agent`）。

当我们使用未被官方完全支持的LLM提供商（如DeepSeek）时，其客户端库（例如配合自定义`base_url`使用的`langchain-openai`）可能无法识别这些额外的参数。这会导致程序因 `TypeError` 异常而崩溃，例如：

- `TypeError: Completions.create() got an unexpected keyword argument 'from_task'`
- `TypeError: Completions.create() got an unexpected keyword argument 'from_agent'`
- `TypeError: ... got multiple values for keyword argument 'callbacks'`

## 解决方案

本补丁引入了一个轻量级的适配器类 `CrewAIFallbackLLM`，它扮演了 CrewAI 和底层LLM客户端之间的“桥梁”角色。

它的工作原理是：在CrewAI调用LLM时进行拦截，并对关键字参数（`kwargs`）进行“清洗”，移除所有已知的不兼容参数，然后再将“干净”的请求转发给真正的LLM实例。这确保了通信的顺畅，让你可以在CrewAI Agent中充分利用DeepSeek的强大能力。

---

## 如何使用

1.  **复制文件**: 将 `deepseek_adapter.py` 文件复制到你的项目中。
2.  **安装依赖**: 确保你安装了所需的依赖包。
    ```bash
    pip install -r requirements.txt
    ```
3.  **配置API密钥**: 在你的项目根目录创建一个名为 `.env` 的文件，并像下面这样加入你的DeepSeek API密钥：

    ```
    # .env
    DEEPSEEK_API_KEY="你的DeepSeek API Key"
    ```

4.  **运行示例**:
    ```bash
    python example.py
    ```

5.  **在你的代码中实现**: 在你的主脚本中，不要直接将 `ChatOpenAI` 实例传递给你的Agent，而是用我们的适配器将它包装起来。请参考 `example.py` 文件查看一个完整、可运行的示例。 