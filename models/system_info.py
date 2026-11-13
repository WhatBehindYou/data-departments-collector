from dataclasses import dataclass, field, fields

@dataclass
class SystemInfo:
    department: str = field(metadata={"label": "Отделение"})
    workplace_name: str = field(metadata={"label": "Наименование"})
    host: str = field(metadata={"label": "IP-адрес"})
    hostname: str = field(metadata={"label": "Имя хоста"})
    kernel: str = field(metadata={"label": "Ядро Linux"})
    printer: str = field(metadata={"label": "Принтер"})
    cpu_temp: str = field(metadata={"label": "Температура CPU"})
    cpu_busy: str = field(metadata={"label": "Загрузка CPU"})

    @classmethod
    def get_headers(cls) -> list[str]:
        return [f.metadata.get("label", f.name) for f in fields(cls)]