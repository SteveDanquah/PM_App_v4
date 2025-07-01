# backend/routers/chat.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_utils import get_llm
from services.prompt_utils import load_prompt
from pinecone import Pinecone
import os

INDEX_HOST = os.getenv("PINECONE_INDEX_HOST") 
router = APIRouter()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(host=INDEX_HOST) 
namespace = "project-plan-analysis"


# ----- INPUT MODEL -----
class ChatRequest(BaseModel):
    question: str


# ----- DOCUMENT ROUTING AGENT -----
def get_relevant_source(user_question: str) -> str:
    prompt = """You are an AI assistant helping route user questions to the most appropriate document type.
Choose from:

1. project_plan_raw_data_group – The raw task list with WBS, resources, completion status at a chunked/grouped level (5 rows at a time). Good for general task queries.
2. milestone_report – A summary of milestone timing and issues. Good for task summaries.
3. validation_report – Feedback on project plan structure and completeness. Good for validation queries.

Return only one:
- "project_plan_raw_data_group"
- "milestone_report"
- "validation_report"

User question: {question}
Answer:
"""
    llm = get_llm()
    result = llm.predict(prompt.format(question=user_question))
    return result.strip().lower()


# ----- ROUTE -----
@router.post("/ask")
def chat_route(payload: ChatRequest):
    question = payload.question
    source = get_relevant_source(question)

    category_mapping = {
        "project_plan_raw_data_group": ["project_plan_raw_data_group"],
        "milestone_report": ["milestone_report"],
        "validation_report": ["validation_report"]
    }

    if source not in category_mapping:
        raise HTTPException(status_code=400, detail="Could not determine source document.")

    try:
        results = index.search(
            namespace=namespace,
            query={
                "inputs": {"text": question},
                "top_k": 20,
                "filter": {"category": {"$in": category_mapping[source]}}
            },
            fields=["text", "category", "chunk_index"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")

    # Build context from matches
    hits = results['result']['hits']
    context_chunks = [hit['fields']['text'] for hit in hits]
    context_text = "\n\n".join(context_chunks)

    # Answer generation
    answer_prompt = """You are an expert project manager and helpful assistant. Use the following project plan context to answer the user's question.

Project Context:
{context}

Question:
{question}

Answer:"""

    llm = get_llm()
    response = llm.predict(answer_prompt.format(context=context_text, question=question))

    return {
        "source_routed_to": source,
        "chunks_used": context_chunks,
        "answer": response
    }
