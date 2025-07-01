import os
import uuid
import re
import pandas as pd
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
NAMESPACE = os.getenv("PINECONE_NAMESPACE")
INDEX_HOST = os.getenv("PINECONE_INDEX_HOST") 

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(host=INDEX_HOST) 


def upsert_project_plan(df: pd.DataFrame, category: str, namespace: str = NAMESPACE):
    row_records = []
    group_records = []

    for i, row in df.iterrows():
        row_text = "\n".join([f"{col}: {row[col]}" for col in df.columns])
        row_records.append({
            "_id": f"RawProjectPlanRow_chunk#{i}",
            "text": row_text,
            "category": f"{category}_row",
            "chunk_index": str(i),
            "source": "project_plan"
        })

    group_size = 5
    for i in range(0, len(df), group_size):
        chunkNum = i // group_size
        group_df = df.iloc[i:i + group_size]
        group_text = "\n\n".join(
            "\n".join([f"{col}: {row[col]}" for col in df.columns])
            for _, row in group_df.iterrows()
        )
        group_records.append({
            "_id": f"RawProjectPlanGroup_chunk#{chunkNum}",
            "text": group_text,
            "category": f"{category}_group",
            "chunk_index": f"group_{i // group_size}",
            "source": "project_plan"
        })

    index.upsert_records(namespace, row_records + group_records)


def upsert_report(report_text: str, category: str, namespace: str = NAMESPACE):
    pattern = r"(?=^## Section: \(\d+(?:\.\d+)?\).*$)"
    section_chunks = re.split(pattern, report_text, flags=re.MULTILINE)
    section_chunks = [chunk.strip() for chunk in section_chunks if chunk.strip()]

    records = []
    for i, chunk in enumerate(section_chunks):
        records.append({
            "_id": f"{category}_chunk#{i}",
            "text": chunk,
            "category": category,
            "chunk_index": str(i),
            "source": category.replace("_report", "")
        })

    index.upsert_records(namespace, records)
