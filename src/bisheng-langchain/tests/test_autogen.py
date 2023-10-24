import os
from bisheng_langchain.autogen_agents import AutoGenAssistantAgent, AutoGenGroupChatManager, AutoGenUserProxyAgent, AutoGenChat

openai_api_key = os.environ.get('OPENAI_API_KEY', '')
openai_proxy = os.environ.get('OPENAI_PROXY', '')


def test_two_agents():
    user_proxy = AutoGenUserProxyAgent("user_proxy",
                                human_input_mode="NEVER",
                                max_consecutive_auto_reply=10,
                                code_execution_flag=True,
                               )

    assistant = AutoGenAssistantAgent("assistant",
                                model_name='gpt-4',
                                openai_api_key=openai_api_key,
                                openai_proxy=openai_proxy,
                                temperature=0)

    chat = AutoGenChat(user_proxy_agent=user_proxy, recipient=assistant)
    # response = chat.run("Plot a chart of NVDA and TESLA stock price change YTD.")
    response = chat.run("今天的日期是什么，距离春节还有多少天？")
    print(response)


def test_group_agents():
    user_proxy = AutoGenUserProxyAgent("Admin",
                                code_execution_flag=False,
                                system_message="A human admin. Interact with the planner to discuss the plan. Plan execution needs to be approved by this admin.",
                               )

    engineer = AutoGenAssistantAgent("Engineer",
                                model_name='gpt-4',
                                openai_api_key=openai_api_key,
                                openai_proxy=openai_proxy,
                                temperature=0,
                                system_message='''Engineer. You follow an approved plan. You write python/shell code to solve tasks. Wrap the code in a code block that specifies the script type. The user can't modify your code. So do not suggest incomplete code which requires others to modify. Don't use a code block if it's not intended to be executed by the executor.
Don't include multiple code blocks in one response. Do not ask others to copy and paste the result. Check the execution result returned by the executor.
If the result indicates there is an error, fix the error and output the code again. Suggest the full code instead of partial code or code changes. If the error can't be fixed or if the task is not solved even after the code is executed successfully, analyze the problem, revisit your assumption, collect additional info you need, and think of a different approach to try.
''')

    scientist = AutoGenAssistantAgent("Scientist",
                                model_name='gpt-4',
                                openai_api_key=openai_api_key,
                                openai_proxy=openai_proxy,
                                temperature=0,
                                system_message="""Scientist. You follow an approved plan. You are able to categorize papers after seeing their abstracts printed. You don't write code.""")

    planner = AutoGenAssistantAgent("Planner",
                                model_name='gpt-4',
                                openai_api_key=openai_api_key,
                                openai_proxy=openai_proxy,
                                temperature=0,
                                system_message="""Planner. Suggest a plan. Revise the plan based on feedback from admin and critic, until admin approval.
The plan may involve an engineer who can write code and a scientist who doesn't write code.
Explain the plan first. Be clear which step is performed by an engineer, and which step is performed by a scientist.""")

    executor = AutoGenUserProxyAgent("Executor",
                                human_input_mode="NEVER",
                                code_execution_flag=True,
                                system_message="Executor. Execute the code written by the engineer and report the result.")

    critic = AutoGenAssistantAgent("Critic",
                                model_name='gpt-4',
                                openai_api_key=openai_api_key,
                                openai_proxy=openai_proxy,
                                temperature=0,
                                system_message="Critic. Double check plan, claims, code from other agents and provide feedback. Check whether the plan includes adding verifiable info such as source URL.")

    manager = AutoGenGroupChatManager(agents=[user_proxy, engineer, scientist, planner, executor, critic], messages=[], max_round=50,
                                model_name='gpt-4',
                                openai_api_key=openai_api_key,
                                openai_proxy=openai_proxy,
                                temperature=0)

    chat = AutoGenChat(user_proxy_agent=user_proxy, recipient=manager)
    response = chat.run("find papers on LLM applications from arxiv in the last week, create a markdown table of different domains.")
    print(response)


test_two_agents()
# test_group_agents()