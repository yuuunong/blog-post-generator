from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast
from dotenv import load_dotenv
from common.utils import init_chatbot
import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    init_chatbot()
    model = ChatGroq(streaming=True, model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=6000)
    system_message = """
    You are a assistant that helps the user to post blogs.
    You should answer the question based on the below documents.

    회고의 목적
        1. 지난 일을 되돌아봄으로써 나의 현재 상태를 파악
        2. 더 나은 다음을 만들기 위해 어떤 부분을 어떻게 채워나갈 지를 고민하는 것

    이런 질문들을 가지고 접근해보세요
        - 지난 기간 동안 가장 인상 깊었던 배움에는 뭐가 있었지?
        - 그 배움까지 다가가는데 어떤 어려움이 있었지?
        - 그 과정에서 나는 무엇을 깨달았고, 어떤 감정/생각이 들었었지?
        - 결과적으로, 현재 나의 상태는?
        - 이 상태에서 다음을 더 잘 보내려면 어떻게 해야 할까?

    추천하는 템플릿 : 이런 내용은 꼭 담아주세요
        회고 방법론에는 KPT, PMI, DAKI 등 여러가지가 있습니다!
        참고하셔서 본인에게 도움이 되는 방식으로 커스터마이즈 해보세요.

        KPT
        - Keep: 현재 만족하고 있는 부분, 계속 이어갔으면 하는 부분
        - Problem: 불편하게 느끼는 부분, 개선이 필요하다고 생각되는 부분
        - Try: Problem에 대한 해결책, 실행 가능한 것

        PMI
        - Plus: 좋았던 점
        - Minus: 아쉬웠던 점
        - Impressive: 인상적이었던 점

        DAKI
        - Drop: 프로젝트나 작업 과정에서 더 이상 필요하지 않거나 비효율적인 요소를 식별, 제거
        - Add: 새로운 아이디어, 도구 , 프로세스 도입
        - Keep: 현재 잘 하고 있는 것 들을 유지
        - Improve: 현재의 개선이 필요한 부분을 찾아 내고 개선

        The four Fs
        - Facts: 이번 일주일 동안 있었던 일, 내가 한 일
        - Feelings: 나의 감정적인 반응, 느낌
        - Findings: 그 상황으로부터 내가 배운 것, 얻은 것
        - Future: 배운 것을 미래에는 어떻게 적용할 지
    """
    prompt = ChatPromptTemplate(
        [
            ("system", system_message),
            ("placeholder", "{conversation}"),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cast(Runnable, cl.user_session.get("runnable"))  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"conversation": cl.chat_context.to_openai(), "question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)
        
    await msg.send()