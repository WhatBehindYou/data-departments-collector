from controllers.monitor_controller import run_departments_check
from config import load_config, DEPARTMENTS_JSON, get_report_path
from models.folders_maker import create_folders

if __name__ == "__main__":
    cfg = load_config()
    create_folders()

    excel_path = get_report_path()
    run_departments_check(DEPARTMENTS_JSON, excel_path, user=cfg.username, password=cfg.password, port=cfg.port)