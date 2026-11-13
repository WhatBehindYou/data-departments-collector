from models.exceptions import HostCheckError
from models.ssh_collector import gather_info
from models.json_handler import json_departments_to_dict
from views.console_view import ConsoleView
from views.excel_view import ExcelView
from pathlib import Path

def run_host_check(console_view: ConsoleView, excel_view: ExcelView, department: str, workplace_name: str, host: str, user: str, password: str, port: int=4220) -> None:
    try:
        info = gather_info(department, workplace_name, host, user, password, port)
        console_view.show_info(info)
        excel_view.append_to_sheet(info)
    except HostCheckError as err:
        console_view.show_error(str(err))

def run_departments_check(departments_filepath: Path | str, excel_path: Path | str, user: str, password: str, port: int) -> None:
    console_view = ConsoleView()
    excel_view = ExcelView(Path(excel_path))

    departments_dict = json_departments_to_dict(Path(departments_filepath))

    for department, workplaces in departments_dict.items():
        for workplace_name, host_ip in workplaces.items():
                run_host_check(console_view, excel_view, department, workplace_name, host_ip, user, password, port)

    excel_view.save()