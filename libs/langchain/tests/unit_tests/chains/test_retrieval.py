"""Test conversation chain and memory."""
from langchain_community.llms.fake import FakeListLLM
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
)

from langchain.chains import create_retrieval_chain
from tests.unit_tests.retrievers.parrot_retriever import FakeParrotRetriever


def test_create() -> None:
    answer = "I know the answer!"
    llm = FakeListLLM(responses=[answer])
    retriever = FakeParrotRetriever()
    question_gen_prompt = PromptTemplate.from_template("hi! {input} {chat_history}")
    chain = create_retrieval_chain(retriever, question_gen_prompt | llm)

    expected_output = {
        "answer": "I know the answer!",
        "chat_history": "foo",
        "context": [Document(page_content="What is the answer?")],
        "input": "What is the answer?",
    }
    output = chain.invoke({"input": "What is the answer?", "chat_history": "foo"})
    assert output == expected_output


def test_create_with_chat_history_messages_only() -> None:
    answer = "I know the answer!"
    llm = FakeListLLM(responses=[answer])
    retriever = FakeParrotRetriever()
    question_gen_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    chain = create_retrieval_chain(retriever, question_gen_prompt | llm)

    expected_output = {
        "answer": "I know the answer!",
        "messages": [
            HumanMessage(content="What is the answer?"),
        ],
        "context": [Document(page_content="What is the answer?")],
    }
    output = chain.invoke(
        {
            "messages": [
                HumanMessage(content="What is the answer?"),
            ],
        }
    )
    assert output == expected_output
