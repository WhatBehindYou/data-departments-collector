from config import REPORTS_DIR

def create_folders():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)