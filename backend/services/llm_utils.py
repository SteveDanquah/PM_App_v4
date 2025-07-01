# backend/services/llm_utils.py

import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv

load_dotenv()


def get_llm():
    return ChatOpenAI(
        model_name="gpt-4.1",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.2
    )


def generate_report(prompt_template: str, plan_json: list) -> str:
    """Generates a report using the provided prompt template and project plan JSON."""
    llm = get_llm()
    prompt = PromptTemplate(input_variables=["project_plan_json"], template=prompt_template)
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({"project_plan_json": plan_json})
