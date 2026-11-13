from pathlib import Path
import json

def json_departments_to_dict(json_file_path: Path | str) -> dict:
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
    return data