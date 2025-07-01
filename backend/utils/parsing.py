import xml.etree.ElementTree as ET
import pandas as pd


def parse_project_xml(file_obj):
    ns = {'msproj': 'http://schemas.microsoft.com/project'}
    tree = ET.parse(file_obj)
    root = tree.getroot()

    resource_map = {
        res.find("msproj:UID", ns).text: res.find("msproj:Name", ns).text
        for res in root.findall(".//msproj:Resource", ns)
        if res.find("msproj:UID", ns) is not None and res.find("msproj:Name", ns) is not None
    }

    assignment_map = {}
    for assign in root.findall(".//msproj:Assignment", ns):
        task_uid = assign.find("msproj:TaskUID", ns)
        resource_uid = assign.find("msproj:ResourceUID", ns)
        if task_uid is not None and resource_uid is not None and resource_uid.text != "0":
            assignment_map.setdefault(task_uid.text, []).append(resource_uid.text)

    tasks = root.findall(".//msproj:Task", ns)
    rows = []

    for task in tasks:
        uid = task.find("msproj:UID", ns)
        if uid is None or uid.text == "0":
            continue

        row = {
            "TASK ID": uid.text,
            "TASK WBS": task.findtext("msproj:WBS", default=None, namespaces=ns),
            "TASK NAME/DESCRIPTION": task.findtext("msproj:Name", default=None, namespaces=ns),
            "MILESTONE": task.findtext("msproj:Milestone", default="0", namespaces=ns) == "1",
            "ASSOCIATED DELIVERABLE": None,
            "START DATE": None,
            "END DATE": None,
            "TASK OWNER": None,
            "TASK STATUS": None,
            "TASK DEPENDENCIES": []
        }

        for ext in task.findall("msproj:ExtendedAttribute", ns):
            value = ext.find("msproj:Value", ns)
            if value is not None:
                row["ASSOCIATED DELIVERABLE"] = value.text
                break

        start = task.find("msproj:ManualStart", ns) or task.find("msproj:Start", ns)
        finish = task.find("msproj:ManualFinish", ns) or task.find("msproj:Finish", ns)
        row["START DATE"] = start.text if start is not None else None
        row["END DATE"] = finish.text if finish is not None else None

        percent = task.find("msproj:PercentComplete", ns)
        if percent is not None:
            pc = int(percent.text)
            row["TASK STATUS"] = (
                "Completed" if pc == 100 else
                "In Progress" if pc > 0 else
                "Not Started"
            )

        preds = [plink.find("msproj:PredecessorUID", ns).text
                 for plink in task.findall("msproj:PredecessorLink", ns)
                 if plink.find("msproj:PredecessorUID", ns) is not None]
        row["TASK DEPENDENCIES"] = preds

        owner_uids = assignment_map.get(uid.text, [])
        owner_names = [resource_map.get(rid) for rid in owner_uids if rid in resource_map]
        row["TASK OWNER"] = ", ".join(owner_names) if owner_names else None

        rows.append(row)

    return pd.DataFrame(rows)
