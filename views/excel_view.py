import openpyxl
from pathlib import Path
from openpyxl.styles import Font
from models.system_info import SystemInfo
from openpyxl.utils.cell import get_column_letter

class ExcelView:
    def __init__(self, filepath: Path | str) -> None:
        self.filepath = Path(filepath)
        self.wb = openpyxl.Workbook()
        # Delete standard first sheet
        self.wb.remove(self.wb.active)

        self.headers = SystemInfo.get_headers()
        self.headers.remove("Отделение")

    def _get_or_create_sheet(self, department: str):
        # Title can not be more than 31 symbols
        sheet_title = department[:31]

        if sheet_title not in self.wb.sheetnames:
            ws = self.wb.create_sheet(title=sheet_title)
            ws.append(self.headers)

            for i in range(1, 20):
                ws.column_dimensions[get_column_letter(i)].width = 26

            # Make headers bold
            for cell in ws[1]:
                cell.font = Font(bold=True)
        return self.wb[sheet_title]

    def append_to_sheet(self, info: SystemInfo) -> None:
        ws = self._get_or_create_sheet(info.department)
        ws.append([
            info.workplace_name,
            info.host,
            info.hostname,
            info.kernel,
            info.printer,
            info.cpu_temp,
            info.cpu_busy
        ])

    def save(self) -> None:
        if not self.wb.sheetnames:
            self.wb.create_sheet("Пустой отчёт")

        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        self.wb.save(self.filepath)


    @staticmethod
    def show_error(message: str) -> None:
        print(f"[ОШИБКА] {message}")
