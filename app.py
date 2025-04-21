from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig
from typing import cast
from dotenv import load_dotenv

import chainlit as cl

load_dotenv()

@cl.on_chat_start
async def on_chat_start():
    model = ChatGroq(streaming=True, model="meta-llama/llama-4-maverick-17b-128e-instruct", max_tokens=6000)
    prompt = ChatPromptTemplate(
        [
            ("system", "You are a helpful assistant."),
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