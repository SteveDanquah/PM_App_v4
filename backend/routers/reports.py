# backend/routers/reports.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import os
import pandas as pd

from services.llm_utils import generate_report
from services.vector_utils import upsert_project_plan, upsert_report
from services.prompt_utils import load_prompt

router = APIRouter()

DATA_DIR = "./data"


@router.post("/generate/{file_id}")
def generate_reports(file_id: str):
    try:
        # Load parsed CSV
        parsed_path = os.path.join(DATA_DIR, f"{file_id}_parsed.csv")
        if not os.path.exists(parsed_path):
            raise HTTPException(status_code=404, detail="Parsed file not found.")

        df = pd.read_csv(parsed_path)
        project_plan_json = df.to_dict(orient="records")

        # Upsert raw project plan
        upsert_project_plan(df, category="project_plan_raw_data", namespace="project-plan-analysis")

        # Generate reports
        validation_prompt = load_prompt("./prompts/validation_prompt.txt")
        milestone_prompt = load_prompt("./prompts/milestone_prompt.txt")

        validation_report = generate_report(prompt_template=validation_prompt, plan_json=project_plan_json)
        milestone_report = generate_report(prompt_template=milestone_prompt, plan_json=project_plan_json)

        # Upsert reports
        upsert_report(validation_report, category="validation_report", namespace="project-plan-analysis")
        upsert_report(milestone_report, category="milestone_report", namespace="project-plan-analysis")

        return JSONResponse(content={
            "message": "Reports generated and chunks upserted to vector DB successfully.",
            "validation_report": validation_report,
            "milestone_report": milestone_report
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
