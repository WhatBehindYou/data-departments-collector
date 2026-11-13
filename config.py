import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.resolve()
DEPARTMENTS_JSON = BASE_DIR / "departments.json"
REPORTS_DIR = BASE_DIR / "reports"
load_dotenv()

@dataclass
class SSHConfig:
    port: int
    username: str
    password: str

def load_config() -> SSHConfig:
    return SSHConfig(
        port=int(os.getenv("SSH_PORT") or 22),
        username=os.getenv("SSH_USER", ""),
        password=os.getenv("SSH_PASSWORD", ""),
    )

def get_report_path() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return REPORTS_DIR / f"report_{timestamp}.xlsx"