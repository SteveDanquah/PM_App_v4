# backend/routers/upload.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import pandas as pd
import os
import uuid
from services.file_utils import parse_excel, parse_xml

router = APIRouter()
load_dotenv()
UPLOAD_DIR = "./data"
os.makedirs(UPLOAD_DIR, exist_ok=True)
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")

@router.post("/")
async def upload_project_plan(file: UploadFile = File(...)):
    filename = file.filename.lower()
    file_id = PINECONE_NAMESPACE + "_" + "RawProjectPlan"
    saved_path = os.path.join(UPLOAD_DIR, f"{file_id}_{filename}")

    with open(saved_path, "wb") as f:
        content = await file.read()
        f.write(content)

    try:
        if filename.endswith(".xlsx"):
            df = parse_excel(saved_path)
        elif filename.endswith(".xml"):
            df = parse_xml(saved_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Store parsed data as CSV for debugging and frontend access
        parsed_path = os.path.join(UPLOAD_DIR, f"{file_id}_parsed.csv")
        df.to_csv(parsed_path, index=False)

        return JSONResponse(content={
            "message": "File uploaded and parsed successfully.",
            "file_id": file_id,
            "columns": df.columns.tolist(),
            "preview": df.head(10).to_dict(orient="records")
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")
