# example.py
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

# 导入我们的兼容性适配器
from deepseek_adapter import CrewAIFallbackLLM

# 从 .env 文件加载环境变量 (其中应包含 DEEPSEEK_API_KEY)
load_dotenv()

# 1. 创建一个标准的 Langchain ChatOpenAI 实例来与 DeepSeek API 通信
try:
    vanilla_deepseek_llm = ChatOpenAI(
        model="deepseek-chat",
        temperature=0,
        api_key=os.environ.get("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com/v1"
    )
except Exception as e:
    print(f"Error creating ChatOpenAI instance: {e}")
    print("Please ensure your DEEPSEEK_API_KEY is set correctly in a .env file.")
    exit()

# 2. 使用我们的适配器包装该实例，使其与CrewAI兼容
crewai_compatible_llm = CrewAIFallbackLLM(llm_instance=vanilla_deepseek_llm)

# 3. 定义一个简单的Agent
# 注意：我们这里不给它任何工具，只为了演示LLM调用是否成功
simple_agent = Agent(
    role='世界级的哲学家',
    goal='用一句话以苏格拉底的风格，对“什么是AI？”这个问题进行回答。',
    backstory='你是一位精通古希腊哲学的学者，擅长用深刻而简洁的语言总结复杂概念。',
    verbose=True,
    memory=False,
    # 将我们包装好的、兼容性强的LLM传递给Agent
    llm=crewai_compatible_llm,
    allow_delegation=False
)

# 4. 定义一个简单的任务
simple_task = Task(
    description='对“什么是AI？”这个问题，给出一个深刻的、苏格拉底式的回答。',
    expected_output='一个包含深刻哲学洞见的、不超过50个字的句子。',
    agent=simple_agent
)

# 5. 组建Crew并启动任务
crew = Crew(
    agents=[simple_agent],
    tasks=[simple_task],
    verbose=2
)

if __name__ == "__main__":
    print("🚀 Starting the philosophical inquiry...")
    print("-----------------------------------------")
    result = crew.kickoff()
    print("\n-----------------------------------------")
    print("✨ Philosophical Inquiry Completed.")
    print("Final Answer:")
    print(result) 