import pandas as pd
from utils.parsing import parse_project_xml


def parse_excel(file_path: str) -> pd.DataFrame:
    """Parse an Excel file into a DataFrame."""
    try:
        df = pd.read_excel(file_path)
        if df.empty:
            raise ValueError("Uploaded Excel file is empty.")
        return df
    except Exception as e:
        raise RuntimeError(f"Error parsing Excel file: {str(e)}")


def parse_xml(file_path: str) -> pd.DataFrame:
    """Parse an XML project plan using existing logic."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            df = parse_project_xml(f)
        if df.empty:
            raise ValueError("Parsed XML returned an empty DataFrame.")
        return df
    except Exception as e:
        raise RuntimeError(f"Error parsing XML file: {str(e)}")
