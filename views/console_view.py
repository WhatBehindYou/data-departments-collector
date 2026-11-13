from models.system_info import SystemInfo

class ConsoleView:
    @staticmethod
    def show_info(info: SystemInfo) -> None:
        print(f"=== Отчет по хосту {info.host} ===")
        print(f"Отделение:       {info.department}")
        print(f"Наименование:    {info.workplace_name}")
        print(f"Имя хоста:       {info.hostname}")
        print(f"Ядро Linux:      {info.kernel}")
        print(f"Принтер:         {info.printer}")
        print(f"Температура CPU: {info.cpu_temp}")
        print(f"Загрузка CPU:    {info.cpu_busy}")
        print("=" * 32)

    @staticmethod
    def show_error(message: str) -> None:
        print(f"[ОШИБКА] {message}")